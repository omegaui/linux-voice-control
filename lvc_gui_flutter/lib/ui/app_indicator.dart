
import 'package:flutter/material.dart';
import 'package:lvc_gui_flutter/main.dart';

class AppIndicator extends StatelessWidget{
  const AppIndicator({super.key});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      width: 30,
      height: 30,
      decoration: BoxDecoration(
        color: inferTagColor(),
        borderRadius: BorderRadius.circular(40),
      ),
    );
  }

}



