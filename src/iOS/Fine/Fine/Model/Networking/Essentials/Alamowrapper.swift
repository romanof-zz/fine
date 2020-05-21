//
//  Alamowrapper.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.

import Foundation
import Alamofire

class Alamowrapper {
    static func request(_ url: URLConvertible, method: Alamofire.HTTPMethod = .get, parameters: Parameters? = nil, encoding: ParameterEncoding? = nil, headers: HTTPHeaders? = [:], auth: BasicAuth?) -> Alamofire.DataRequest {
     
        let methodEncoding: ParameterEncoding
        if method == .get {
            methodEncoding = URLEncoding.default
        } else {
            methodEncoding = JSONEncoding.default
        }
        let decidedEncoding = encoding ?? methodEncoding
        

        var headerWithToken: [String: String]? = headers
        if headerWithToken == nil {
            headerWithToken = [:]
        }
        let request = Alamofire.request(url, method: method, parameters: parameters, encoding: decidedEncoding, headers: headerWithToken)
        if let auth = auth {
            request.authenticate(user: auth.username, password: auth.password)
        }
        return request
    }
}
