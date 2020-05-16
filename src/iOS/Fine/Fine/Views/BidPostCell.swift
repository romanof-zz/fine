//
//  BidPostCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

class BidPostCell: BasePostCell {

    @IBOutlet weak var userBkgView: UIView!
    @IBOutlet weak var userLabel: UILabel!
    @IBOutlet weak var activityLabel: UILabel!
    @IBOutlet weak var dateLabel: UILabel!

    @IBOutlet weak var likeButton: UIButton!

    @IBOutlet weak var bidButon: UIButton!
    @IBOutlet weak var commentButton: UIButton!

    private var actions: [String: String] = ["buy": "bought", "sell": "sold", "": "error"]

    private var post: Post?

    override func setup(with post: Post) {
        self.post = post

        userBkgView.backgroundColor = post.user.color
        userLabel.text = post.user.initials.uppercased()

        let userName = post.user.name ?? "error"
        let bidAction = post.details.action ?? ""
        let bidActionThirdForm = actions[bidAction] ?? "error"
        let bidSymbol = post.details.symbol?.uppercased() ?? ""
        let bidPrice = post.details.price ?? 0
        let bidPriceString = String(format: "%.3f", bidPrice)

        let activityText = "\(userName) \(bidActionThirdForm) \(bidSymbol) at $\(bidPriceString)"
        activityLabel.attributedText = Utils.attributedString(from: activityText, stringAttributes: [
                (userName, [NSAttributedString.Key.font: UIFont.systemFont(ofSize: 18, weight: .semibold)]),
                       (bidSymbol, [NSAttributedString.Key.font: UIFont.systemFont(ofSize: 18, weight: .semibold)])
                       ])
        dateLabel.text = Date(timeIntervalSince1970: TimeInterval(post.timestamp)).timeAgoDisplay()

        likeButton.setTitle(": \(post.likesCount)", for: .normal)
        let imageName = post.isLiked ? "icon_liked" :  "icon_like"
        likeButton.setImage(UIImage(named: imageName), for: .normal)

        commentButton.setTitle("comments: \(post.commentsCount)", for: .normal)

        updateBidState()
    }

    @IBAction func likeTapped(_ sender: Any) {
        guard let post = post else { return }

        //toggle
        post.isLiked = !post.isLiked

        let imageName = post.isLiked ? "icon_liked" : "icon_like"
        likeButton.setImage(UIImage(named: imageName), for: .normal)

        let plusCount = post.isLiked ? 1 : 0
        likeButton.setTitle(": \(post.likesCount + plusCount)", for: .normal)

        Utils.bounceView(likeButton)
    }

    @IBAction func bidTapped(_ sender: Any) {

        post?.isBidded = !(post?.isBidded ?? false)
        updateBidState()

        Utils.bounceView(bidButon)
        Utils.showPopup(with: "BID MADE", and: "icon_bidded")
    }

    @IBAction func commentsTapped(_ sender: Any) {
        let commentsVC: CommentsViewController = Utils.instantiateVC(from: "Main")
        commentsVC.comments = post?.comments ?? []
        guard let tabbar = UIApplication.shared.keyWindow?.rootViewController as? UITabBarController, let navbar = tabbar.selectedViewController as? UINavigationController else { return }

        navbar.pushViewController(commentsVC, animated: true)
    }

    // MARK: Private
    private func updateBidState() {
        let isBidded = post?.isBidded ?? false
        bidButon.setTitle(isBidded ? "BID MADE" : "BID", for: .normal)
        bidButon.setImage(isBidded ? UIImage(named: "icon_bidded") : nil, for: .normal)
        bidButon.isEnabled = !isBidded
    }
}
