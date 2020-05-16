//
//  FeedViewController.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

private enum FeedPostCellType: String {
    case bid
    case video
}

class FeedViewController: BaseViewController {

    @IBOutlet weak var tableView: UITableView!

    private(set) var posts: [Post] = []

    private var cellTypes: [FeedPostCellType: BasePostCell.Type] = [.bid : BidPostCell.self,
                                                                .video: VideoPostCell.self]

    private let refreshControl = UIRefreshControl()

    override func viewDidLoad() {
        super.viewDidLoad()

        tableView.refreshControl = refreshControl
        refreshControl.addTarget(self, action: #selector(refreshPosts), for: .valueChanged)
        refreshControl.tintColor = .white

        tableView.separatorInset = UIEdgeInsets(top: 0, left: 20, bottom: 0, right: 20)
        tableView.tableFooterView = UIView()
        tableView.rowHeight = UITableView.automaticDimension
        tableView.estimatedRowHeight = 200
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        refreshPosts()
    }

    @objc private func refreshPosts() {
        DataManager.shared.networkManager.fetchPosts {[weak self] (response) in
            self?.refreshControl.endRefreshing()

            switch response {
            case .Success(let posts):
                self?.posts = posts
                self?.tableView.reloadData()
            case .Error(_):
                Utils.showAlert(with: "Error fetching feed")
            }
        }
    }
}

extension FeedViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return posts.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {

        let post = posts[indexPath.row]
        guard let postCellType = FeedPostCellType(rawValue: post.type),
            let cellClass = cellTypes[postCellType],
            let cell = tableView.dequeueReusableCell(withIdentifier: cellClass.identifier, for: indexPath) as? BasePostCell
            else { return UITableViewCell() }


        cell.setup(with: post)

        return cell
    }
}

extension FeedViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }
}
