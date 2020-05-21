//
//  Comment.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

class Comment: FBaseModel {
    var user: User
    var text: String
    var timestamp: Double
    var isLiked: Bool
    var likesCount: Int

    private enum CodingKeys: String, CodingKey {
        case user, text, timestamp, isLiked = "is_liked", likesCount = "like_cnt"
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        text = try container.decode(String.self, forKey: .text)
        timestamp = try container.decode(Double.self, forKey: .timestamp)

        user = try container.decode(User.self, forKey: .user)

        isLiked = try container.decode(Bool.self, forKey: .isLiked)
        likesCount = try container.decode(Int.self, forKey: .likesCount)

        try super.init(from: decoder)
    }

    init(id: Int, user: User, text: String, timestamp: Double, isLiked: Bool, likesCount: Int) {
        self.user = user
        self.text = text
        self.timestamp = timestamp
        self.isLiked = isLiked
        self.likesCount = likesCount

        super.init(id: id)
    }
}
