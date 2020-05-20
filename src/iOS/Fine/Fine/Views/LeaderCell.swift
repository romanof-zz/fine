//
//  LeaderCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 20/05/2020.
//

import UIKit

class LeaderCell: BaseTableViewCell {
    
    @IBOutlet weak var valueLabel: UILabel!
    @IBOutlet weak var followButton: UIButton!
    @IBOutlet weak var leaderImageView: UIImageView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var descLabel: UILabel!
    @IBOutlet weak var followActivityIndicator: UIActivityIndicatorView!

    private var expert: Expert?

    @IBOutlet weak var noImageUserView: UIView!
    @IBOutlet weak var noImageUserLabel: UILabel!

    override func awakeFromNib() {
        super.awakeFromNib()
        leaderImageView.image = UIImage(named: "icon_user")?.withRenderingMode(.alwaysTemplate)
    }

    override func prepareForReuse() {
        super.prepareForReuse()
        leaderImageView.tintColor = .main
    }

    func setup(with expert: Expert) {
        self.expert = expert

        redraw()
    }

    private func redraw() {
        guard let expert = expert else { return }
        nameLabel.text = expert.name
        descLabel.text = expert.desc
        descLabel.isHidden = expert.desc == nil
        
        valueLabel.text = "\(expert.value)"
        followButton.isEnabled = !expert.isFollowed
        followButton.backgroundColor = expert.isFollowed ? .lightGray : .main

        noImageUserView.isHidden = false
        noImageUserLabel.text = expert.initials.uppercased()
        leaderImageView.isHidden = true

        if let imageUrl = expert.imageUrl, let url = URL(string: imageUrl) {

            leaderImageView.af_setImage(withURL: url, placeholderImage: nil, filter: nil, progress: nil, progressQueue: DispatchQueue.main, imageTransition: .crossDissolve(0.3), runImageTransitionIfCached: true) {[weak self] (response) in
                if response.value != nil {
                    self?.leaderImageView.isHidden = false
                    self?.noImageUserView.isHidden = true
                }
            }
        }
    }

    @IBAction func followTapped(_ sender: Any) {
        followButton.isHidden = true
        followActivityIndicator.isHidden = false
        followActivityIndicator.startAnimating()

        expert?.isFollowed = true
        redraw()

        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {[weak self] in
            self?.followButton.isHidden = false
            self?.followActivityIndicator.isHidden = true
            self?.followActivityIndicator.stopAnimating()

        }
    }
}
