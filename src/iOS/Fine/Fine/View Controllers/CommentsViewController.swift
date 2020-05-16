//
//  CommentsViewController.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit
import IHKeyboardAvoiding

class CommentsViewController: BaseViewController {

    @IBOutlet weak var commentView: UIView!
    @IBOutlet weak var commentButton: UIButton!
    @IBOutlet weak var commentsTextView: UITextField!
    @IBOutlet weak var tableView: UITableView!

    var comments: [Comment] = []

    override func viewDidLoad() {
        super.viewDidLoad()

        tableView.separatorInset = UIEdgeInsets(top: 0, left: 20, bottom: 0, right: 20)
        tableView.tableFooterView = UIView()
        tableView.rowHeight = UITableView.automaticDimension
        tableView.estimatedRowHeight = 200

        KeyboardAvoiding.avoidingView = commentView

        commentsTextView.addTarget(self, action: #selector(commentsTextViewChanged), for: .editingChanged)
    }

    @objc private func commentsTextViewChanged() {
        commentButton.isEnabled = (commentsTextView.text?.count ?? 0) > 0
    }

    @IBAction func sendTapped(_ sender: Any) {
        guard let user = comments.first?.user else { return }
        let comment = Comment(id: 112, user: user, text: commentsTextView.text ?? "", timestamp: Date.timeIntervalSinceReferenceDate, isLiked: false, likesCount: 0)
        comments.append(comment)
        tableView.reloadData()

        commentsTextView.text = nil
        commentButton.isEnabled = false
    }
}

extension CommentsViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return comments.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {

        let comment = comments[indexPath.row]
        guard let cell = tableView.dequeueReusableCell(withIdentifier: CommentCell.identifier, for: indexPath) as? CommentCell else { return UITableViewCell() }

        cell.setup(with: comment)

        return cell
    }
}

extension CommentsViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }
}

