import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class PinScreen extends StatefulWidget {
  const PinScreen({super.key});

  @override
  State<PinScreen> createState() => _PinScreenState();
}

class _PinScreenState extends State<PinScreen> {
  final List<String> _pin = [];
  static const _maxPinLength = 6;

  void _onKeyTap(String digit) {
    if (_pin.length < _maxPinLength) {
      setState(() => _pin.add(digit));
    }
  }

  void _onBackspace() {
    if (_pin.isNotEmpty) {
      setState(() => _pin.removeLast());
    }
  }

  void _onSubmit() {
    // TODO: wire to auth API in the next step
    if (_pin.length >= 4) {
      context.go('/home');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Enter your PIN', style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(_maxPinLength, (i) {
                  final filled = i < _pin.length;
                  return Container(
                    margin: const EdgeInsets.symmetric(horizontal: 6),
                    width: 16,
                    height: 16,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: filled
                          ? Theme.of(context).colorScheme.primary
                          : Theme.of(context).colorScheme.primary.withOpacity(0.2),
                    ),
                  );
                }),
              ),
              const SizedBox(height: 40),
              _buildKeypad(),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _pin.length >= 4 ? _onSubmit : null,
                child: const Text('Unlock'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildKeypad() {
    final keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', '⌫'];
    return GridView.count(
      shrinkWrap: true,
      crossAxisCount: 3,
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      physics: const NeverScrollableScrollPhysics(),
      children: keys.map((key) {
        if (key.isEmpty) return const SizedBox.shrink();
        return InkWell(
          borderRadius: BorderRadius.circular(40),
          onTap: () => key == '⌫' ? _onBackspace() : _onKeyTap(key),
          child: Container(
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: Theme.of(context).cardTheme.color,
            ),
            child: Center(
              child: Text(key, style: Theme.of(context).textTheme.titleLarge),
            ),
          ),
        );
      }).toList(),
    );
  }
}
