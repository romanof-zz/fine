//
//  FUser.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.
//  Copyright © 2020 Romanof. All rights reserved.
//

import UIKit

class User: Decodable, Equatable {
    var id: Int
    var name: String?
    var type: String?

    static func == (lhs: User, rhs: User) -> Bool {
        lhs.id == rhs.id
    }

    private enum CodingKeys: String, CodingKey {
        case id = "user_id"
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(Int.self, forKey: .id)
    }
}
