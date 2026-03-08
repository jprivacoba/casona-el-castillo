import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'theme.dart';

class AboutSection extends StatelessWidget {
  const AboutSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: AppTheme.cream,
      padding: const EdgeInsets.symmetric(vertical: 72, horizontal: 40),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          // Imagen con altura fija
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Image.asset(
                'assets/images/quienes-somos.jpg',
                height: 380,
                fit: BoxFit.cover,
                cacheWidth: 700,
              ),
            ),
          ),
          const SizedBox(width: 56),
          // Texto
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _sectionLabel('QUIÉNES SOMOS'),
                const SizedBox(height: 16),
                Text(
                  'Nuestra Historia',
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
                const SizedBox(height: 8),
                Container(width: 48, height: 2, color: AppTheme.gold),
                const SizedBox(height: 24),
                Text(
                  'Casona Fundo El Castillo nace del sueño familiar de devolverle vida a un parque con más de 80 años de historia. Diseñado por un paisajista francés y rodeado de árboles centenarios, este lugar único combina patrimonio, naturaleza y elegancia.',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
                const SizedBox(height: 16),
                Text(
                  'Nuestra antigua casona ha sido cuidadosamente restaurada, integrando modernos baños y una cocina de más de 300 m², creando el escenario perfecto para eventos inolvidables.',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class LocationSection extends StatelessWidget {
  const LocationSection({super.key});

  // Coordenadas de Fundo El Castillo, Calle Larga, Los Andes
  static final LatLng _location = LatLng(-32.8850, -70.6494);

  @override
  Widget build(BuildContext context) {
    return Container(
      color: AppTheme.creamAlt,
      padding: const EdgeInsets.symmetric(vertical: 72, horizontal: 40),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _sectionLabel('UBICACIÓN'),
          const SizedBox(height: 16),
          Text(
            'Dónde encontrarnos',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 8),
          Container(width: 48, height: 2, color: AppTheme.gold),
          const SizedBox(height: 32),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Mapa interactivo
              Expanded(
                flex: 3,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: SizedBox(
                    height: 340,
                    child: FlutterMap(
                      options: MapOptions(
                        initialCenter: _location,
                        initialZoom: 14,
                      ),
                      children: [
                        TileLayer(
                          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                          userAgentPackageName: 'com.casona.app',
                        ),
                        MarkerLayer(
                          markers: [
                            Marker(
                              point: _location,
                              width: 48,
                              height: 56,
                              child: const _MapPin(),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 32),
              // Info
              Expanded(
                flex: 2,
                child: Container(
                  height: 340,
                  decoration: BoxDecoration(
                    color: AppTheme.white,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: const Color(0xFFE0D5C5)),
                  ),
                  child: const Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.location_on, size: 40, color: AppTheme.gold),
                      SizedBox(height: 16),
                      Text(
                        'Calle Larga',
                        style: TextStyle(
                          fontSize: 20,
                          fontFamily: 'Playfair Display',
                          fontWeight: FontWeight.w600,
                          color: AppTheme.dark,
                        ),
                      ),
                      SizedBox(height: 6),
                      Text(
                        'Los Andes, Valparaíso',
                        style: TextStyle(color: AppTheme.muted, fontSize: 14),
                      ),
                      SizedBox(height: 24),
                      Divider(indent: 32, endIndent: 32, color: Color(0xFFE0D5C5)),
                      SizedBox(height: 24),
                      Padding(
                        padding: EdgeInsets.symmetric(horizontal: 24),
                        child: Text(
                          'A 80 km de Santiago.\nAcceso fácil por Ruta 60.',
                          textAlign: TextAlign.center,
                          style: TextStyle(color: AppTheme.muted, fontSize: 13, height: 1.7),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _MapPin extends StatelessWidget {
  const _MapPin();

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 36,
          height: 36,
          decoration: const BoxDecoration(
            color: AppTheme.gold,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(color: Colors.black26, blurRadius: 6, offset: Offset(0, 3)),
            ],
          ),
          child: const Icon(Icons.villa_outlined, color: Colors.white, size: 20),
        ),
        CustomPaint(
          size: const Size(12, 8),
          painter: _TrianglePainter(),
        ),
      ],
    );
  }
}

class _TrianglePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = AppTheme.gold;
    final path = ui.Path()
      ..moveTo(0, 0)
      ..lineTo(size.width, 0)
      ..lineTo(size.width / 2, size.height)
      ..close();
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(_) => false;
}

Widget _sectionLabel(String text) {
  return Text(
    text,
    style: const TextStyle(
      fontSize: 11,
      letterSpacing: 2.5,
      color: AppTheme.gold,
      fontWeight: FontWeight.w700,
    ),
  );
}
