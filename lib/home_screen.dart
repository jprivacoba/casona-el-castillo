import 'package:flutter/material.dart';
import 'theme.dart';

class HomeScreen extends StatelessWidget {
  final VoidCallback? onContactTap;
  const HomeScreen({super.key, this.onContactTap});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Imagen hero
        SizedBox(
          height: 520,
          width: double.infinity,
          child: Image.asset(
            'assets/images/hero.jpg',
            fit: BoxFit.cover,
            cacheWidth: 1400,
          ),
        ),
        // Gradiente oscuro
        Container(
          height: 520,
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Color(0x77000000),
                Color(0xCC000000),
              ],
            ),
          ),
        ),
        // Contenido centrado
        SizedBox(
          height: 520,
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Línea decorativa + label con fondo para contraste
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  decoration: BoxDecoration(
                    color: Colors.black.withValues(alpha: 0.35),
                    borderRadius: BorderRadius.circular(2),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(width: 40, height: 1, color: AppTheme.gold),
                      const SizedBox(width: 14),
                      const Text(
                        'CENTRO DE EVENTOS · CHILE',
                        style: TextStyle(
                          color: AppTheme.gold,
                          fontSize: 11,
                          letterSpacing: 3.5,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      const SizedBox(width: 14),
                      Container(width: 40, height: 1, color: AppTheme.gold),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                Text(
                  'Casona Fundo\nEl Castillo',
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.displayLarge?.copyWith(
                        color: Colors.white,
                        fontSize: 68,
                        height: 1.05,
                        shadows: const [
                          Shadow(
                            color: Color(0x88000000),
                            blurRadius: 20,
                            offset: Offset(0, 4),
                          ),
                        ],
                      ),
                ),
                const SizedBox(height: 16),
                const Text(
                  'Historia, naturaleza y elegancia\nen un parque francés centenario.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Color(0xCCFFFFFF),
                    fontSize: 16,
                    height: 1.6,
                    letterSpacing: 0.3,
                  ),
                ),
                const SizedBox(height: 36),
                OutlinedButton(
                  onPressed: onContactTap,
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.white,
                    side: const BorderSide(color: AppTheme.gold, width: 1.5),
                    padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(4),
                    ),
                  ),
                  child: const Text(
                    'SOLICITAR INFORMACIÓN',
                    style: TextStyle(
                      fontSize: 12,
                      letterSpacing: 2,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
