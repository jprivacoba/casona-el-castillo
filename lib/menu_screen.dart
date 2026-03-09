import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'theme.dart';

class MenuScreen extends StatelessWidget {
  const MenuScreen({super.key});

  Future<void> _launchURL(String url) async {
    final Uri uri = Uri.base.resolve(Uri.encodeFull(url));
    if (!await launchUrl(uri, webOnlyWindowName: '_blank')) {
      throw Exception('Could not launch $url');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'EXPERIENCIAS',
            style: Theme.of(context).textTheme.bodySmall?.copyWith(letterSpacing: 0.2),
          ),
          const SizedBox(height: 8),
          Text(
            'Nuestras Cartas',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 16),
          Text(
            'Cocina de campo chilena con acentos contemporáneos.',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 32),
          _buildMenuCard(
            context,
            'Pack Asado',
            'Ideal para celebraciones al fuego lento.',
            'assets/images/foto asado.jpg',
            'assets/assets/docs/pack asado.pdf',
          ),
          const SizedBox(height: 16),
          _buildMenuCard(
            context,
            'Pack Fundo El Castillo',
            'Experiencia gastronómica completa en la casona.',
            'assets/images/foto pack.jpg',
            'assets/assets/docs/pack fundo el castillo.pdf',
          ),
        ],
      ),
    );
  }

  Widget _buildMenuCard(BuildContext context, String title, String subtitle, String imagePath, String pdfUrl) {
    return GestureDetector(
      onTap: () => _launchURL(pdfUrl),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 10,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          children: [
            Image.asset(
              imagePath,
              height: 180,
              width: double.infinity,
              fit: BoxFit.cover,
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(title, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontSize: 18)),
                        Text(subtitle, style: const TextStyle(color: AppTheme.muted)),
                      ],
                    ),
                  ),
                  const Icon(Icons.picture_as_pdf_outlined, color: AppTheme.olive),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
