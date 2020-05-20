//
//  CommentCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

class CommentCell: BaseTableViewCell {

    @IBOutlet weak var likeButton: UIButton!
    @IBOutlet weak var dateLabel: UILabel!
    @IBOutlet weak var commentLabel: UILabel!
    @IBOutlet weak var userBkgView: UIView!
    @IBOutlet weak var userLabel: UILabel!

    var comment: Comment?

    func setup(with comment: Comment) {
        self.comment = comment

        userBkgView.backgroundColor = comment.user.color
        userLabel.text = comment.user.initials.uppercased()

        commentLabel?.text = comment.text
        
        dateLabel.text = Date(timeIntervalSince1970: TimeInterval(comment.timestamp)).timeAgoDisplay()

        let imageName = comment.isLiked ? "icon_liked" :  "icon_like"
        likeButton.setImage(UIImage(named: imageName), for: .normal)
        likeButton.setTitle(": \(comment.likesCount)", for: .normal)
    }

    @IBAction func likeTapped(_ sender: Any) {
        guard let comment = comment else { return }

        //toggle
        comment.isLiked = !comment.isLiked

        let imageName = comment.isLiked ? "icon_liked" : "icon_like"
        likeButton.setImage(UIImage(named: imageName), for: .normal)

        let plusCount = comment.isLiked ? 1 : -1
        comment.likesCount += plusCount
        likeButton.setTitle(": \(comment.likesCount)", for: .normal)

        Utils.bounceView(likeButton)
    }
}
