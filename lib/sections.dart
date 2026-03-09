import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:url_launcher/url_launcher.dart';
import 'theme.dart';

class AboutSection extends StatelessWidget {
  const AboutSection({super.key});

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Container(
      color: AppTheme.cream,
      padding: EdgeInsets.symmetric(
        vertical: isMobile ? 48 : 72,
        horizontal: isMobile ? 20 : 40,
      ),
      child: isMobile ? _buildMobile(context) : _buildDesktop(context),
    );
  }

  Widget _buildDesktop(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
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
        Expanded(child: _buildText(context)),
      ],
    );
  }

  Widget _buildMobile(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: Image.asset(
            'assets/images/quienes-somos.jpg',
            height: 240,
            width: double.infinity,
            fit: BoxFit.cover,
            cacheWidth: 700,
          ),
        ),
        const SizedBox(height: 32),
        _buildText(context),
      ],
    );
  }

  Widget _buildText(BuildContext context) {
    return Column(
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
    );
  }
}

class LocationSection extends StatefulWidget {
  const LocationSection({super.key});

  @override
  State<LocationSection> createState() => _LocationSectionState();
}

class _LocationSectionState extends State<LocationSection> {
  static final LatLng _location = LatLng(-32.8850, -70.6494);
  final MapController _mapController = MapController();

  void _openInMaps() {
    final uri = Uri.parse(
      'https://www.google.com/maps/search/?api=1&query=${_location.latitude},${_location.longitude}',
    );
    launchUrl(uri, mode: LaunchMode.externalApplication);
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Container(
      color: AppTheme.creamAlt,
      padding: EdgeInsets.symmetric(
        vertical: isMobile ? 48 : 72,
        horizontal: isMobile ? 20 : 40,
      ),
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
          if (isMobile) _buildMobile() else _buildDesktop(),
        ],
      ),
    );
  }

  Widget _buildDesktop() {
    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            flex: 3,
            child: _buildMap(isMobile: false),
          ),
          const SizedBox(width: 32),
          Expanded(
            flex: 2,
            child: _buildInfoCard(),
          ),
        ],
      ),
    );
  }

  Widget _buildMobile() {
    return Column(
      children: [
        _buildMap(isMobile: true),
        const SizedBox(height: 16),
        _buildInfoCard(),
      ],
    );
  }

  Widget _buildMap({required bool isMobile}) {
    // Móvil: solo dos dedos (un dedo hace scroll de página)
    // Desktop: scroll wheel + drag completo
    final interactionFlags = isMobile
        ? InteractiveFlag.pinchZoom |
          InteractiveFlag.pinchMove |
          InteractiveFlag.doubleTapZoom
        : InteractiveFlag.scrollWheelZoom |
          InteractiveFlag.pinchZoom |
          InteractiveFlag.drag |
          InteractiveFlag.doubleTapZoom;

    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: SizedBox(
        height: isMobile ? 240 : 340,
        child: Stack(
          children: [
            FlutterMap(
              mapController: _mapController,
              options: MapOptions(
                initialCenter: _location,
                initialZoom: 14,
                interactionOptions: InteractionOptions(
                  flags: interactionFlags,
                ),
              ),
              children: [
                TileLayer(
                  // ESRI World Topo Map (terrain)
                  urlTemplate:
                      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
                  userAgentPackageName: 'com.casona.app',
                ),
                MarkerLayer(
                  markers: [
                    Marker(
                      point: _location,
                      width: 48,
                      height: 56,
                      child: GestureDetector(
                        onTap: _openInMaps,
                        child: const _MapPin(),
                      ),
                    ),
                  ],
                ),
              ],
            ),
            // Botones de zoom (solo desktop)
            if (!isMobile)
              Positioned(
                right: 12,
                bottom: 24,
                child: _ZoomButtons(controller: _mapController),
              ),
            // Indicador móvil
            if (isMobile)
              Positioned(
                bottom: 8,
                left: 0,
                right: 0,
                child: Center(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.black54,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      'Usa dos dedos para mover el mapa',
                      style: TextStyle(color: Colors.white70, fontSize: 11),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoCard() {
    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        color: AppTheme.white,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFFE0D5C5)),
      ),
      padding: const EdgeInsets.symmetric(vertical: 32, horizontal: 24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.location_on, size: 40, color: AppTheme.gold),
          const SizedBox(height: 16),
          const Text(
            'Calle Larga',
            style: TextStyle(
              fontSize: 20,
              fontFamily: 'Playfair Display',
              fontWeight: FontWeight.w600,
              color: AppTheme.dark,
            ),
          ),
          const SizedBox(height: 6),
          const Text(
            'Los Andes, Valparaíso',
            style: TextStyle(color: AppTheme.muted, fontSize: 14),
          ),
          const SizedBox(height: 24),
          const Divider(indent: 32, endIndent: 32, color: Color(0xFFE0D5C5)),
          const SizedBox(height: 24),
          const Text(
            'A 80 km de Santiago.\nAcceso fácil por Ruta 60.',
            textAlign: TextAlign.center,
            style: TextStyle(color: AppTheme.muted, fontSize: 13, height: 1.7),
          ),
          const SizedBox(height: 20),
          OutlinedButton.icon(
            onPressed: _openInMaps,
            icon: const Icon(Icons.map_outlined, size: 16),
            label: const Text('Abrir en Google Maps'),
            style: OutlinedButton.styleFrom(
              foregroundColor: AppTheme.dark,
              side: const BorderSide(color: AppTheme.gold),
              textStyle: const TextStyle(fontSize: 12, letterSpacing: 0.5),
            ),
          ),
        ],
      ),
    );
  }
}

class _ZoomButtons extends StatelessWidget {
  final MapController controller;
  const _ZoomButtons({required this.controller});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _ZoomButton(
          icon: Icons.add,
          onTap: () => controller.move(
            controller.camera.center,
            controller.camera.zoom + 1,
          ),
        ),
        const SizedBox(height: 4),
        _ZoomButton(
          icon: Icons.remove,
          onTap: () => controller.move(
            controller.camera.center,
            controller.camera.zoom - 1,
          ),
        ),
      ],
    );
  }
}

class _ZoomButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;
  const _ZoomButton({required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 32,
        height: 32,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(4),
          boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 4)],
        ),
        child: Icon(icon, size: 18, color: AppTheme.dark),
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
