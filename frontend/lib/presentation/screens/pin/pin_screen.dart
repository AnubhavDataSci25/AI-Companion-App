import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../providers/app_providers.dart';

class PinScreen extends ConsumerStatefulWidget {
  const PinScreen({super.key});

  @override
  ConsumerState<PinScreen> createState() => _PinScreenState();
}

class _PinScreenState extends ConsumerState<PinScreen> {
  final List<String> _pin = [];
  final _nameController = TextEditingController();
  static const _maxPinLength = 6;
  bool _loading = false;
  String? _error;

  void _onKeyTap(String digit) {
    if (_pin.length < _maxPinLength) {
      setState(() {
        _pin.add(digit);
        _error = null;
      });
    }
  }

  void _onBackspace() {
    if (_pin.isNotEmpty) {
      setState(() => _pin.removeLast());
    }
  }

  Future<void> _onSubmit() async {
    if (_nameController.text.trim().isEmpty) {
      setState(() => _error = 'Enter your name first.');
      return;
    }
    if (_pin.length < 4) return;

    setState(() {
      _loading = true;
      _error = null;
    });

    final authRepo = ref.read(authRepositoryProvider);
    final error = await authRepo.login(_nameController.text.trim(), _pin.join());

    if (!mounted) return;
    setState(() => _loading = false);

    if (error != null) {
      setState(() {
        _error = error;
        _pin.clear();
      });
    } else {
      context.go('/home');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          child: Column(
            children: [
              const SizedBox(height: 20),
              Text('Welcome to Ami', style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 20),
              TextField(
                controller: _nameController,
                decoration: const InputDecoration(hintText: 'Your name'),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              Text('Enter your PIN', style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 16),
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
              if (_error != null) ...[
                const SizedBox(height: 12),
                Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
              ],
              const SizedBox(height: 24),
              _buildKeypad(),
              const SizedBox(height: 24),
              _loading
                  ? const CircularProgressIndicator()
                  : ElevatedButton(
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