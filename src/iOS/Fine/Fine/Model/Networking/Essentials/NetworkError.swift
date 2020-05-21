//
//  NetworkError.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.

import Foundation

public struct NetworkError: GenericError {
    
    public enum NetworkErrorType {
        case noNetwork
        case blocked
        case userWasLoggedOut
        case generic
        case parsing
    }
    
    let type: NetworkErrorType
    
    public init(type: NetworkErrorType) {
        self.type = type
    }
    
    public func localizedErrorDescription() -> String {
        switch type {
        case .noNetwork:
            return NSLocalizedString("error.noNetwork.message", comment: "")
        case .blocked:
            return NSLocalizedString("error.blocked.message", comment: "")
        case .userWasLoggedOut:
            return NSLocalizedString("error.forcelogout", comment: "")
        case .generic:
            return NSLocalizedString("error.network.generic.message", comment: "")
        case .parsing:
            return NSLocalizedString("error.network.parsing.message", comment: "")
        }
    }
    
    public func localizedErrorTitle() -> String {
        switch self {
        default:
            return NSLocalizedString("error.network.generic.title", comment: "")
        }
    }
}
