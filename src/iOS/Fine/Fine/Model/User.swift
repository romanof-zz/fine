//
//  User.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

class User: Decodable, Equatable {
    var id: Int = 0
    var name: String?
    var type: String?

    static func == (lhs: User, rhs: User) -> Bool {
        lhs.id == rhs.id
    }

    private enum CodingKeys: String, CodingKey {
        case id = "user_id", name, type
    }

//    required init(from decoder: Decoder) throws {
//        let container = try decoder.container(keyedBy: CodingKeys.self)
//        id = try container.decode(Int.self, forKey: .id)
//        name = try?
//    }

    // MARK: //

    var color: UIColor  {
        if let hexColor = DataManager.shared.userColors[id] {
            return UIColor(hex: hexColor)
        }

        return .yellow
    }

    var initials: String {
        guard let name = name else { return "??" }

        let nameComps = name.components(separatedBy: " ")
        if nameComps.count == 2 {
            return String(nameComps[0].prefix(1) + nameComps[1].prefix(1))
        } else {
            return String(name.prefix(2))
        }
    }
}
