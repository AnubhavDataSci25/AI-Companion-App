import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorageService {
  final _storage = const FlutterSecureStorage();
  static const _tokenKey = 'session_token';
  static const _roleKey = 'user_role';

  Future<void> saveSession(String token, String role) async {
    await _storage.write(key: _tokenKey, value: token);
    await _storage.write(key: _roleKey, value: role);
  }

  Future<String?> getToken() => _storage.read(key: _tokenKey);
  Future<String?> getRole() => _storage.read(key: _roleKey);

  Future<void> clearSession() async {
    await _storage.delete(key: _tokenKey);
    await _storage.delete(key: _roleKey);
  }
}