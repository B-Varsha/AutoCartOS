import 'package:flutter/material.dart';

class LogoWidget extends StatelessWidget {
  const LogoWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: const [
        Icon(Icons.shopping_cart_checkout_rounded,
            size: 70, color: Color(0xff6366f1)),
        SizedBox(height: 8),
        Text(
          "",
          style: TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        Text(
          " ",
          style: TextStyle(color: Colors.white54),
        )
      ],
    );
  }
}
