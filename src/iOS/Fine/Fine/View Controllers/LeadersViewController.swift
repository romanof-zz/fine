//
//  LeadersViewController.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 20/05/2020.
//

import UIKit

class LeadersViewController: BaseViewController {

    @IBOutlet weak var tableView: UITableView!
    private let refreshControl = UIRefreshControl()

    private var leaders: [[Expert]] = [[], []]

    private var sectionNames = ["EXPERTS", "LEADERBOARD"]

    override func viewDidLoad() {
        super.viewDidLoad()

        tableView.refreshControl = refreshControl
        refreshControl.addTarget(self, action: #selector(refreshLeaders), for: .valueChanged)
        refreshControl.tintColor = .white

        tableView.separatorInset = UIEdgeInsets(top: 0, left: 20, bottom: 0, right: 20)
        tableView.tableFooterView = UIView()
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)

        refreshLeaders()
    }

    @objc private func refreshLeaders() {
        DataManager.shared.networkManager.fetchExperts {[weak self] (response) in
            self?.refreshControl.endRefreshing()

            switch response {
            case .Success(let experts):
                self?.leaders[0] = experts
                self?.tableView.reloadData()
            case .Error(_):
                Utils.showAlert(with: "Error fetching experts")
            }
        }

        DataManager.shared.networkManager.fetchUsers {[weak self] (response) in
            self?.refreshControl.endRefreshing()

            switch response {
            case .Success(let users):
                self?.leaders[1] = users
                self?.tableView.reloadData()
            case .Error(_):
                Utils.showAlert(with: "Error fetching experts")
            }
        }
    }
}

extension LeadersViewController: UITableViewDataSource {
    func numberOfSections(in tableView: UITableView) -> Int {
        return 2
    }
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return leaders[section].count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: LeaderCell.identifier, for: indexPath) as? LeaderCell else { return UITableViewCell() }

        let leader = leaders[indexPath.section][indexPath.row]
        cell.setup(with: leader)

        return cell
    }
}

extension LeadersViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }

    func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        switch section {
        case 0:
            return "EXPERTS"
        default:
            return "LEADERBOARD"
        }
    }

    func tableView(_ tableView: UITableView, willDisplayHeaderView view: UIView, forSection section: Int) {
        let headerView = view as! UITableViewHeaderFooterView
        headerView.textLabel?.font = UIFont.boldSystemFont(ofSize: 20)
        headerView.textLabel?.textColor = .white
    }
}

