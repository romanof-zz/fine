//
//  GraphCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit
import ILG

class GraphCell: BaseTableViewCell {
    private var portfolio: Portfolio?

    private var buttons: [UIButton] = []

    @IBOutlet weak var interactionValueLabel: UILabel!
    @IBOutlet weak var buttonsStack: UIStackView!
    @IBOutlet weak var graphPlaceholder: UIView!

    private let graphView = InteractiveLineGraphView()

    override func awakeFromNib() {
        super.awakeFromNib()

        graphPlaceholder.addSubview(graphView)
        graphView.frame = graphPlaceholder.bounds
        graphView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        graphView.interactionDelegate = self
    }

    override func prepareForReuse() {
        super.prepareForReuse()
        for button in buttons {
            button.removeFromSuperview()
        }
        buttons.removeAll()
    }

    func setup(with portfolio: Portfolio) {
        self.portfolio = portfolio

        for key in portfolio.timeSeries.keys.sorted() {
            let button = UIButton(frame: CGRect(x: 0, y: 0, width: 60, height: 40))
            button.setTitle(key, for: .normal)

            button.setTitleColor(.orange, for: .normal)
            button.setTitleColor(.white, for: .selected)

            button.clipsToBounds = true
            button.layer.cornerRadius = 5
            button.addTarget(self, action: #selector(buttonTapped), for: .touchUpInside)
            buttonsStack.addArrangedSubview(button)
            buttons.append(button)
        }

        if let firstButton = buttonsStack.arrangedSubviews[0] as? UIButton {
            firstButton.isSelected = true
            firstButton.backgroundColor = .systemOrange

            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {[weak self] in
                self?.buttonTapped(firstButton)
            }

        }
    }

    @objc func buttonTapped(_ sender: UIButton) {
        for view in buttonsStack.arrangedSubviews {
            guard let button = view as? UIButton else { return }
            button.isSelected = false
            button.backgroundColor = .clear
        }
        sender.isSelected = true
        sender.backgroundColor = .systemOrange


        let series = sender.titleLabel?.text ?? ""
        updateGraph(for: series)
    }

    private var currentValues: [Double] = []

    private func updateGraph(for series: String) {
        guard let portfolio = portfolio else { return }
        guard let data = portfolio.timeSeries[series] else { return }

        currentValues = data.map { (key, value) -> Double in
            if let doubleValue = value as? Double {
                return doubleValue
            } else if let intValue = value as? Int {
                return Double(intValue)
            } else {
                assert(true)
                return 0
            }
        }

        graphView.update(withDataPoints: currentValues, animated: true)
    }

    private var hideTimer: Timer?
}


extension GraphCell: GraphViewInteractionDelegate {
    func graphViewInteraction(userInputDidChange currentIndex: Int) {
        print(currentValues[currentIndex])

        interactionValueLabel.alpha = 1
        interactionValueLabel.text = String(format: "$%.02f", currentValues[currentIndex])
        hideTimer = Timer.scheduledTimer(withTimeInterval: 1, repeats: false, block: {[weak self] (timer) in
            UIView.animate(withDuration: 0.6) {[weak self] in
                self?.interactionValueLabel.alpha = 0
            }
        })
    }
}
