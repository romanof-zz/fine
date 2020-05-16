//
//  FComment.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.
//  Copyright © 2020 Romanof. All rights reserved.
//

import UIKit

class Comment: FBaseModel {
    var user: User
    var text: String
    var timestamp: Int
    var isLiked: Bool
    var likesCount: Int

    private enum CodingKeys: String, CodingKey {
        case user, text, timestamp, isLiked = "is_liked", likesCount = "like_cnt"
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        text = try container.decode(String.self, forKey: .text)
        timestamp = try container.decode(Int.self, forKey: .timestamp)

        user = try container.decode(User.self, forKey: .user)

        isLiked = try container.decode(Bool.self, forKey: .isLiked)
        likesCount = try container.decode(Int.self, forKey: .likesCount)

        try super.init(from: decoder)
    }

}
