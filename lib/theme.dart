import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  static const Color cream = Color(0xFFFAF7F3);       // Fondo principal cálido
  static const Color creamAlt = Color(0xFFF3EBE0);    // Fondo alternado secciones
  static const Color gold = Color(0xFFB8935A);         // Acento dorado
  static const Color goldLight = Color(0xFFD4B483);   // Dorado claro
  static const Color sage = Color(0xFF6B7A5C);         // Verde salvia
  static const Color dark = Color(0xFF1E1710);         // Marrón oscuro premium
  static const Color text = Color(0xFF2A2118);         // Texto principal
  static const Color muted = Color(0xFF8A8077);        // Texto secundario
  static const Color white = Colors.white;

  // Aliases de compatibilidad
  static const Color beige = cream;
  static const Color beigeSoft = creamAlt;
  static const Color olive = dark;
  static const Color sageDark = sage;

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: dark,
        primary: dark,
        surface: cream,
      ),
      scaffoldBackgroundColor: cream,
      textTheme: GoogleFonts.sourceSans3TextTheme().copyWith(
        displayLarge: GoogleFonts.playfairDisplay(
          fontSize: 46,
          fontWeight: FontWeight.bold,
          color: text,
          fontStyle: FontStyle.italic,
          height: 1.15,
        ),
        headlineMedium: GoogleFonts.playfairDisplay(
          fontSize: 30,
          fontWeight: FontWeight.w600,
          color: text,
          height: 1.2,
        ),
        titleLarge: GoogleFonts.playfairDisplay(
          fontSize: 22,
          fontWeight: FontWeight.w600,
          color: text,
        ),
        bodyLarge: GoogleFonts.sourceSans3(
          fontSize: 17,
          color: text,
          height: 1.75,
        ),
        bodyMedium: GoogleFonts.sourceSans3(
          fontSize: 15,
          color: text,
          height: 1.75,
        ),
        bodySmall: GoogleFonts.sourceSans3(
          fontSize: 11,
          color: gold,
          letterSpacing: 2,
          fontWeight: FontWeight.w700,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: dark,
          foregroundColor: white,
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(4),
          ),
          elevation: 0,
          textStyle: GoogleFonts.sourceSans3(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            letterSpacing: 1,
          ),
        ),
      ),
    );
  }
}
