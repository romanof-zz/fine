//
//  Post.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

class PostDetails: Decodable {
    var symbol: String?
    var price: Float?
    var action: String?
    var url: String?
}

class Post: FBaseModel {
    var type: String
    var timestamp: TimeInterval

    var user: User
    var details: PostDetails

    var isLiked: Bool
    var likesCount: Int
    var commentsCount: Int
    var comments: [Comment]?

    var isBidded: Bool?
    
    private enum CodingKeys: String, CodingKey {
        case type, timestamp, user, details, isLiked = "is_liked", likesCount = "like_cnt", commentsCount = "comment_cnt" , comments, isBidded = "is_bidded"
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        type = try container.decode(String.self, forKey: .type)
        timestamp = try container.decode(TimeInterval.self, forKey: .timestamp)

        user = try container.decode(User.self, forKey: .user)
        details = try container.decode(PostDetails.self, forKey: .details)
        comments = try? container.decode([Comment].self, forKey: .comments)

        isLiked = try container.decode(Bool.self, forKey: .isLiked)
        likesCount = try container.decode(Int.self, forKey: .likesCount)
        commentsCount = try container.decode(Int.self, forKey: .commentsCount)

        isBidded = try? container.decode(Bool.self, forKey: .isBidded)

        try! super.init(from: decoder)
    }
}
