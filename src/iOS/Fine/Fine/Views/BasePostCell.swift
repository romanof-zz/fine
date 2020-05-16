//
//  BasePostCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

class BasePostCell: BaseTableViewCell {
    func setup(with post: Post) {
        //do nothing, virtual method
    }

    class var cellHeight: CGFloat {
        return 0
    }
}
