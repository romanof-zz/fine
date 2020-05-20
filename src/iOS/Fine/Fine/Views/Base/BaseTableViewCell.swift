//
//  BaseTableViewCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

class BaseTableViewCell: UITableViewCell, IdentifierProtocol {
}

protocol IdentifierProtocol {
    static var identifier: String { get }
}

extension IdentifierProtocol {
    static var identifier: String {
        return String(describing: self)
    }
}
