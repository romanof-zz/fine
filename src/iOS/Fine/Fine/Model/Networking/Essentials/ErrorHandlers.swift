//
//  GenericErrorHandler.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.

import Foundation

public protocol ErrorHandler {
    func errorFor(statusCode: Int?) -> GenericError
}

public struct GenericErrorHandler: ErrorHandler {
    public init() {
    }
    
    public func errorFor(statusCode: Int?) -> GenericError {
        return NetworkError(type:.generic)
    }
}
