//
//  Utils.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit
import StatusAlert

class Utils: NSObject {
    
    // MARK: Alerts
    class func showAlert(with title: String?, _ message: String? = nil, _ completion: (()->Void)? = nil) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
        UIApplication.shared.windows[0].rootViewController?.present(alert, animated: true, completion: completion)
    }
    
    // MARK: UI and strings
    class func attributedString(from source: String, stringAttributes: [(String?, [NSAttributedString.Key: Any])]) -> NSAttributedString {
        let result = NSMutableAttributedString(string: source)
        
        for stringAttribute in stringAttributes {
            
            if let substring = stringAttribute.0, let stringRange = source.range(of: substring) {
                let range = NSRange(stringRange, in: source)
                
                let attributesDictionary = stringAttribute.1
                
                for attribute in attributesDictionary {
                    result.addAttribute(attribute.key, value: attribute.value, range: range)
                }
            }
        }
        return result
    }
    
    class func showPopup(with title: String?, and imageName: String?) {
        // Creating StatusAlert instance
        let statusAlert = StatusAlert()
        if let imageName = imageName {
            statusAlert.image = UIImage(named: imageName)
        }
        
        statusAlert.title = title
        statusAlert.alertShowingDuration = 0.6
        //        statusAlert.message = "Message to show beyond title"
        //statusAlert.canBePickedOrDismissed = isUserInteractionAllowed
        
        // Presenting created instance
        statusAlert.showInKeyWindow()
        
    }
    
    // MARK: Storyboards
    class func instantiateVC<T: UIViewController>(from: String) -> T {
        return UIStoryboard.init(name: from, bundle: nil).instantiateVC()
    }
    
    class func bounceView(_ view: UIView, for duration: TimeInterval = 0.3) {
        UIView.animate(withDuration: duration, delay: 0, usingSpringWithDamping: 0.6, initialSpringVelocity: 0.6, options: [.autoreverse, .beginFromCurrentState], animations: {
            view.transform = CGAffineTransform(scaleX: 1.6, y: 1.6)
        }, completion: { (finished) in
            view.transform = .identity
        })
    }
}
