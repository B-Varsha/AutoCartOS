import 'package:flutter/material.dart';

class ProductCard extends StatelessWidget {
  final Map product;
  const ProductCard({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xff1e293b),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          const Icon(Icons.inventory_2, color: Color(0xff6366f1), size: 40),
          const SizedBox(width: 15),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(product["name"],
                    style: const TextStyle(
                        fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 5),
                Text(product["component"],
                    style: const TextStyle(color: Colors.white54)),
              ],
            ),
          ),
          Text("\$${product["price"]}",
              style: const TextStyle(
                  color: Color(0xff22c55e),
                  fontWeight: FontWeight.bold,
                  fontSize: 16))
        ],
      ),
    );
  }
}
