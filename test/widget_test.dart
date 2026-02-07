import 'package:flutter_test/flutter_test.dart';
import 'package:cartpilot_app/main.dart';

void main() {
  testWidgets('CartPilot loads correctly', (WidgetTester tester) async {
    await tester.pumpWidget(const AutoCartOSApp());

    expect(find.text('CartPilot AI'), findsOneWidget);
  });
}
