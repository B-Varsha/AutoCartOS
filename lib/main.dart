import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'widgets/logo.dart';
import 'widgets/product_card.dart';
import 'widgets/summary_card.dart';

void main() {
  runApp(const AutoCartOSApp());
}

class AutoCartOSApp extends StatelessWidget {
  const AutoCartOSApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "AutoCartOS",
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xff0f172a),
        primaryColor: const Color(0xff6366f1),
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final controller = TextEditingController();

  Map<String, dynamic>? autoCartResult;
  bool loading = false;

  Future generateAutoCart() async {
    if (controller.text.isEmpty) return;

    setState(() => loading = true);

    try {
      final data = await ApiService.generateCart(controller.text);
      setState(() => autoCartResult = data);
    } catch (e) {
      debugPrint(e.toString());
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Backend not reachable")),
      );
    }

    setState(() => loading = false);
  }

  @override
  Widget build(BuildContext context) {
    final products = autoCartResult?["cart"] ?? [];

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 40),
                       /// 🚀 LOGO
              const LogoWidget(),

              const SizedBox(height: 30),

              const Text(
                "AutoCartOS",
                style: TextStyle(
                  fontSize: 34,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.2,
                ),
              ),

              const SizedBox(height: 10),

              const Text(
                "AI-Powered Industrial Procurement Assistant",
                style: TextStyle(
                  color: Colors.white70,
                  fontSize: 16,
                ),
              ),

              const SizedBox(height: 40),

     

              /// 🔎 USER INPUT
              TextField(
                controller: controller,
                style: const TextStyle(fontSize: 16),
                decoration: InputDecoration(
                  hintText:
                      "Describe your industrial problem (electrical, safety, testing, security...)",
                  filled: true,
                  fillColor: const Color(0xff1e293b),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(18),
                    borderSide: BorderSide.none,
                  ),
                  contentPadding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 18),
                ),
              ),

              const SizedBox(height: 20),

              /// ⚡ GENERATE BUTTON
              ElevatedButton(
                onPressed: generateAutoCart,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xff6366f1),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(18)),
                ),
                child: const Text(
                  "Generate AutoCart",
                  style: TextStyle(fontSize: 16),
                ),
              ),

              const SizedBox(height: 30),

              /// ⏳ LOADING STATE
              if (loading)
                const Column(
                  children: [
                    CircularProgressIndicator(),
                    SizedBox(height: 12),
                    Text("Building your AutoCart..."),
                  ],
                ),

              const SizedBox(height: 20),

              /// 📊 RESULTS UI
              if (autoCartResult != null) ...[
                SummaryCard(result: autoCartResult!),
                const SizedBox(height: 20),
                ...products
                    .map<Widget>((p) => ProductCard(product: p))
                    .toList(),
              ]
            ],
          ),
        ),
      ),
    );
  }
}

