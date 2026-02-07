import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const baseUrl = "http://10.0.2.2:8000";

  static Future<Map<String, dynamic>> generateCart(String prompt) async {
    final response = await http.post(
      Uri.parse("$baseUrl/generate-cart"), // 🔥 FIXED HERE
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"user_goal": prompt}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to generate cart");
    }
  }
}


