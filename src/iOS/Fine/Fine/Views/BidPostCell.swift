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

    override func awakeFromNib() {
        super.awakeFromNib()

        bidButon.titleLabel?.adjustsFontSizeToFitWidth = true
    }
    
    override func setup(with post: Post) {
        self.post = post

        userBkgView.backgroundColor = post.user.color
        userLabel.text = post.user.initials.uppercased()

        let userName = post.user.name ?? "error"
        let bidAction = post.details.action ?? ""
        let bidActionThirdForm = actions[bidAction] ?? "error"
        let bidSymbol = post.details.symbol?.uppercased() ?? ""
        let bidPrice = post.details.price ?? 0
        let bidPriceString = String(format: "%.2f", bidPrice)

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

        let plusCount = post.isLiked ? 1 : -1
        post.likesCount += plusCount
        likeButton.setTitle(": \(post.likesCount)", for: .normal)

        Utils.bounceView(likeButton)
    }

    @IBAction func bidTapped(_ sender: Any) {
        showBidAlert()
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

    private func showBidAlert() {
        guard let post = post else { return }

        let bidSymbol = post.details.symbol?.uppercased() ?? ""
        let bidPrice = post.details.price ?? 0
        let bidPriceString = String(format: "%.2f", bidPrice)

        let vc = UIViewController()
        vc.preferredContentSize = CGSize(width: 250,height: 250)
        let pickerView = UIPickerView(frame: CGRect(x: 0, y: 0, width: 250, height: 250))
        pickerView.delegate = self
        pickerView.dataSource = self
        pickerView.selectRow(9, inComponent: 0, animated: true)
        vc.view.addSubview(pickerView)
        let pickerAlert = UIAlertController(title: "\(bidSymbol) at $\(bidPriceString)", message: "some short help message", preferredStyle: .alert)
        pickerAlert.setValue(vc, forKey: "contentViewController")

        pickerAlert.addAction(UIAlertAction(title: "MAKE BID", style: .default, handler: {[weak self] (_) in
            guard let `self` = self else { return }

            self.post?.isBidded = !(self.post?.isBidded ?? false)
            self.updateBidState()

            Utils.bounceView(self.bidButon)
            Utils.showPopup(with: "BID MADE", and: "icon_bidded")

            DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                guard let tabbar = UIApplication.shared.keyWindow?.rootViewController as? UITabBarController,
                    let navVC = tabbar.viewControllers?[1] as? UINavigationController,
                    let portfolioVC = navVC.viewControllers[0] as? PortfolioViewController
                    else { return }

                tabbar.selectedIndex = 1

                let selectedPickerIndex = pickerView.selectedRow(inComponent: 0)
                let bidValue = Double(selectedPickerIndex) / 10.0 + 0.1

                portfolioVC.showBid(["symbol": bidSymbol, "value": bidValue])
            }
        }))

        pickerAlert.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))

        UIApplication.shared.keyWindow?.rootViewController?.present(pickerAlert, animated: true)
    }
}

extension BidPostCell: UIPickerViewDataSource, UIPickerViewDelegate {
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }

    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return 1000
    }

    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        let stringValue = String(format: "%.1f %%", Float(row) / 10.0 + 0.1)
        return stringValue
    }
}
