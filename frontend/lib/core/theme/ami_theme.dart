import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'ami_colors.dart';

class AmiTheme {
  static ThemeData get light => _buildTheme(
        brightness: Brightness.light,
        background: AmiColors.lightBackground,
        primary: AmiColors.lightPrimary,
        secondary: AmiColors.lightSecondary,
        text: AmiColors.lightText,
      );

  static ThemeData get dark => _buildTheme(
        brightness: Brightness.dark,
        background: AmiColors.darkBackground,
        primary: AmiColors.darkPrimary,
        secondary: AmiColors.darkSecondary,
        text: AmiColors.darkText,
      );

  static ThemeData _buildTheme({
    required Brightness brightness,
    required Color background,
    required Color primary,
    required Color secondary,
    required Color text,
  }) {
    final base = ThemeData(brightness: brightness, useMaterial3: true);

    return base.copyWith(
      scaffoldBackgroundColor: background,
      colorScheme: base.colorScheme.copyWith(
        primary: primary,
        secondary: secondary,
        surface: background,
      ),
      textTheme: GoogleFonts.nunitoTextTheme(base.textTheme).apply(
        bodyColor: text,
        displayColor: text,
      ),
      cardTheme: CardThemeData(
        color: brightness == Brightness.light ? Colors.white : secondary.withOpacity(0.2),
        elevation: 2,
        shadowColor: Colors.black.withOpacity(0.08),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: brightness == Brightness.light ? AmiColors.lightText : Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: brightness == Brightness.light ? Colors.white : secondary.withOpacity(0.15),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide.none,
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      ),
    );
  }
}
