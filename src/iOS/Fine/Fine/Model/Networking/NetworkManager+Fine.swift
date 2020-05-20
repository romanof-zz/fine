//
//  NetworkManager+Posts.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

fileprivate enum FineEndpoints: String, CaseIterable {
    case posts = "/posts"
    case portfolio = "/portfolio"
    case user = "/user"
    case experts = "/experts"
    case users = "/users"
    
    //post
    case like = "/like"
    case comment = "/comment"
    case bid = "/bid"
    case follow = "/follow"
}

extension NetworkManager {
    func fetchPosts(_ completion: @escaping (_ response: GenericResponse<[Post]>) -> Void) {
        let endpoint = Endpoint<[Post]>(urlPath: FineEndpoints.posts.rawValue, pathParameter: nil, parameterList: nil, method: .get, errorHandler: GenericErrorHandler())
        middleware.sendResponseNetworkCall(endpoint: endpoint, completion: completion)
    }

    func fetchPortfolio(_ completion: @escaping (_ response: GenericResponse<Portfolio>) -> Void) {
        let endpoint = Endpoint<Portfolio>(urlPath: FineEndpoints.portfolio.rawValue, pathParameter: nil, parameterList: nil, method: .get, errorHandler: GenericErrorHandler())
        middleware.sendResponseNetworkCall(endpoint: endpoint, completion: completion)
    }

    func fetchUser(_ completion: @escaping (_ response: GenericResponse<User>) -> Void) {
        let endpoint = Endpoint<User>(urlPath: FineEndpoints.user.rawValue, pathParameter: nil, parameterList: nil, method: .get, errorHandler: GenericErrorHandler())
        middleware.sendResponseNetworkCall(endpoint: endpoint, completion: completion)
    }

    func fetchExperts(_ completion: @escaping (_ response: GenericResponse<[Expert]>) -> Void) {
        let endpoint = Endpoint<[Expert]>(urlPath: FineEndpoints.experts.rawValue, pathParameter: nil, parameterList: nil, method: .get, errorHandler: GenericErrorHandler())
        middleware.sendResponseNetworkCall(endpoint: endpoint, completion: completion)
    }

    func fetchUsers(_ completion: @escaping (_ response: GenericResponse<[Expert]>) -> Void) {
        let endpoint = Endpoint<[Expert]>(urlPath: FineEndpoints.users.rawValue, pathParameter: nil, parameterList: nil, method: .get, errorHandler: GenericErrorHandler())
        middleware.sendResponseNetworkCall(endpoint: endpoint, completion: completion)
    }

//    func likePost(with id: String, _ completion: @escaping (_ response: GenericResponse<[Post]>) -> Void) {
//
//    }
}
