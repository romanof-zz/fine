//
//  Middleware.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.

import Foundation
import Alamofire

public struct BasicAuth {
    var username: String
    var password: String
    
    public init(username: String, password: String) {
        self.username = username
        self.password = password
    }
}

struct DateTransformer {
    
    static let iso8601: DateFormatter = {
        let formatter = DateFormatter()
        formatter.calendar = Calendar(identifier: .iso8601)
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.timeZone = TimeZone(secondsFromGMT: 0)
        formatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss" // 2018-01-30T22:00:00.000Z
        return formatter
    }()
}

public struct Endpoint <T> {
    var urlPath: String
    var pathParameter: String?
    var parameterList: [String: Any]?
    var method: HTTPMethod
    var errorHandler: ErrorHandler?
    var saveCookies: Bool = false
    var auth: BasicAuth?
    
    public init(urlPath: String, pathParameter: String? = nil, parameterList: [String: Any]? = nil, method: HTTPMethod, saveCookies: Bool = false, errorHandler: ErrorHandler? = GenericErrorHandler(), auth: BasicAuth? = nil) {
        self.urlPath = urlPath
        self.pathParameter = pathParameter
        self.parameterList = parameterList
        self.method = method
        self.errorHandler = errorHandler
        self.saveCookies = saveCookies
        self.auth = auth
    }
    
    func getFullPath(baseURL: String, apiVersion: String) -> String {
        if let pathParameter = pathParameter {
            return "\(baseURL)\(apiVersion)\(urlPath)/\(pathParameter)"
        }
        return "\(baseURL)\(apiVersion)\(urlPath)"
    }
}

public class NetworkMiddleware {
    
    fileprivate let baseURL: String
    fileprivate let apiVersion: String
//    fileprivate let modelMapper: NewModelMapper
    
    fileprivate let blockedStatusValue: Int
    fileprivate let forceLogoutStatusValue: Int
    fileprivate let kCookiesKey = "Cookies"
    
    public init(baseURL: String, apiVersion: String, blockedStatusValue: Int = 418, forceLogoutStatusValue: Int = 417) {
        self.baseURL = baseURL
        self.apiVersion = apiVersion
        
        self.blockedStatusValue = blockedStatusValue
        self.forceLogoutStatusValue = forceLogoutStatusValue
        
        restoreCookies()
    }
    
    public class func isConnected() -> Bool {
        return NetworkReachabilityManager()!.isReachable
    }
    
    public func sendResponseNetworkCall<T:Decodable>(endpoint: Endpoint<T>, completion:@escaping (_ response: GenericResponse<T>) -> Void ) {
        if !NetworkMiddleware.isConnected() {
            completion(GenericResponse.Error(NetworkError(type:.noNetwork)))
            return
        }
        
        let fullURL = endpoint.getFullPath(baseURL: baseURL, apiVersion: apiVersion)
        let params: [String: Any]? = endpoint.parameterList
        
        Alamowrapper.request(fullURL, method: endpoint.method, parameters: params, auth: endpoint.auth)
            .responseJSON { (response: DataResponse<Any>) in
                if endpoint.saveCookies {
                    self.saveCookies()
                }
                self.handleResponse(response: response, endpoint: endpoint, completion: completion)
        }
    }
    
    func handleResponse<T: Decodable>(response: DataResponse<Any>, endpoint: Endpoint<T>,  completion:@escaping (_ response: GenericResponse<T>) -> Void ) {
        
        switch response.result {
        case .success:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .formatted(DateTransformer.iso8601)
            let response: GenericResponse<T>  = decoder.decodeResponse(from: response)
            completion(response)
        case .failure:
            let statusCode = response.response?.statusCode
            switch statusCode {
            case self.blockedStatusValue:
                completion(GenericResponse.Error(NetworkError(type:.blocked)))
            case self.forceLogoutStatusValue:
                NotificationCenter.default.post(name: NSNotification.Name(rawValue: "ForceLogout"), object: nil)
                completion(GenericResponse.Error(NetworkError(type:.userWasLoggedOut)))
            default:
                let error = endpoint.errorHandler?.errorFor(statusCode: statusCode) ?? NetworkError(type:.blocked)
                completion(GenericResponse.Error(error))
            }
        }
    }
 
    //MARK: Convenience methods
    fileprivate func saveCookies() {
        guard let baseUrl = URL(string: self.baseURL),
            let cookies = HTTPCookieStorage.shared.cookies(for: baseUrl) else { return }

        var cookiesDic = UserDefaults.standard.dictionary(forKey: kCookiesKey) ?? [:]

        for cookie in cookies {
            cookiesDic[cookie.name] = cookie.properties
        }
        UserDefaults.standard.set(cookiesDic, forKey: kCookiesKey)
    }

    fileprivate func restoreCookies() {
        guard let baseUrl = URL(string: self.baseURL) else { return }

        let cookiesDic = UserDefaults.standard.dictionary(forKey: kCookiesKey) ?? [:]

        var cookies: [HTTPCookie] = []
        for cookieProps in cookiesDic.values {
            if let cookieProps = cookieProps as? [HTTPCookiePropertyKey: Any],
                let cookie = HTTPCookie(properties: cookieProps) {
                cookies.append(cookie)
            }
        }
        HTTPCookieStorage.shared.setCookies(cookies, for: baseUrl, mainDocumentURL: nil)
    }
    
}
