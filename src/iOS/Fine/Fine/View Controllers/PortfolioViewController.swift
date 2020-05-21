//
//  PortfolioViewController.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit

private enum PortfolioPostCellType: String {
    case stock
}


class PortfolioViewController: BaseViewController {

    private let refreshControl = UIRefreshControl()
    @IBOutlet weak var tableView: UITableView!

    var portfolio: Portfolio?

    private var percentMode = false

    override func viewDidLoad() {
        super.viewDidLoad()

        tableView.refreshControl = refreshControl
        refreshControl.addTarget(self, action: #selector(refreshPortfolio), for: .valueChanged)
        refreshControl.tintColor = .white

        tableView.separatorInset = UIEdgeInsets(top: 0, left: 20, bottom: 0, right: 20)
        tableView.tableFooterView = UIView()
        tableView.rowHeight = UITableView.automaticDimension
        tableView.estimatedRowHeight = 200

    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        refreshPortfolio()
    }

    @objc private func refreshPortfolio() {
        DataManager.shared.networkManager.fetchPortfolio {[weak self] (response) in
            self?.refreshControl.endRefreshing()

            switch response {
            case .Success(let portfolio):
                self?.portfolio = portfolio
                self?.tableView.reloadData()
            case .Error(_):
                Utils.showAlert(with: "Error fetching portfolio")
            }
        }
    }

    func showBid(_ with: [String: Any]) {
        let action = {[weak self] in
            guard let symbol = with["symbol"] as? String,
                let bidValue = with["value"] as? Double else { return }

            if let cellIndex = self?.portfolio?.stocks.firstIndex(where: { (stockItem) -> Bool in
                return stockItem.symbol.uppercased() == symbol.uppercased()
                }) {

                self?.animateBid(bidValue, at: cellIndex)
            }
        }

        if !isViewLoaded {
            loadView()

            DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
                action()
            }
        } else {
            action()
        }
    }

    private var bidValueToAnimate: Double?
    private var cellIndexToAnimate: Int?
    private func animateBid(_ bidValue: Double, at cellIndex: Int) {

        bidValueToAnimate = bidValue
        cellIndexToAnimate = cellIndex

        let indexPath = IndexPath(row: cellIndex, section: 2)
        tableView.scrollToRow(at: indexPath, at: .middle, animated: true)
//        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {[weak self] in
//            self?.tableView.reloadRows(at: [indexPath], with: .automatic)
//        }

    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        bidValueToAnimate = nil
        cellIndexToAnimate = nil
    }
}

extension PortfolioViewController: UITableViewDataSource {

    func numberOfSections(in tableView: UITableView) -> Int {
        3
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        switch section {
        case 0:
            return 1
        case 1:
            return 1
        case 2:
            return portfolio?.stocks.count ?? 0
        default:
            return 0
        }
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let portfolio = portfolio else { return UITableViewCell() }

        switch indexPath.section {
        case 0:
            guard let cell = tableView.dequeueReusableCell(withIdentifier: ValueCell.identifier, for: indexPath) as? ValueCell else { return UITableViewCell() }
            cell.setup(with: portfolio)
            return cell
        case 1:
            guard let cell = tableView.dequeueReusableCell(withIdentifier: GraphCell.identifier, for: indexPath) as? GraphCell else { return UITableViewCell() }
            cell.setup(with: portfolio)
            return cell
        case 2:
            guard let cell = tableView.dequeueReusableCell(withIdentifier: StockCell.identifier, for: indexPath) as? StockCell else { return UITableViewCell() }
            cell.setup(with: portfolio.stocks[indexPath.row], percentMode: percentMode)

            if let bidValueToAnimate = bidValueToAnimate,
                let cellIndexToAnimate = cellIndexToAnimate, cellIndexToAnimate == indexPath.row {
                cell.animateBid(bidValueToAnimate)
            }
            return cell
        default:
            let cell = UITableViewCell()
            cell.backgroundColor = .red
            return cell
        }
    }
}

extension PortfolioViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        percentMode = !percentMode
        tableView.reloadData()
    }

    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        switch indexPath.section {
        case 0:
            return 80
        case 1:
            return 260
        case 2:
            return 80
        default:
            return 0
        }
    }
}
