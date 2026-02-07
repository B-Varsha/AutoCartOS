import 'package:flutter/material.dart';

class SummaryCard extends StatelessWidget {
  final Map result;
  const SummaryCard({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: const Color(0xff1e293b),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("Cart Summary",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          Text(result["cart_summary"] ?? ""),
          const SizedBox(height: 8),
          Text("Total Price: \$${result["total_price"]}",
              style: const TextStyle(
                  fontSize: 18, color: Color(0xff22c55e))),
        ],
      ),
    );
  }
}

