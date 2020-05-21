//
//  ValueCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit

class ValueCell: BaseTableViewCell {


    @IBOutlet weak var valueLabel: UILabel!

    func setup(with portfolio: Portfolio) {
        let percent = (portfolio.value.close - portfolio.value.open) / portfolio.value.close
        valueLabel.text = String(format: "$%.02f (%0.2f%%)", portfolio.value.close, percent)
        valueLabel.textColor = percent > 0 ? UIColor(red: 52/255.0, green: 128/255.0, blue: 90/255.0, alpha: 1.0) : .red
    }
}
