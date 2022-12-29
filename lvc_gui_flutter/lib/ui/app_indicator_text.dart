

import 'package:flutter/material.dart';
import 'package:lvc_gui_flutter/main.dart';
import 'package:lvc_gui_flutter/themex.dart';

class AppIndicatorText extends StatelessWidget{
  const AppIndicatorText({super.key});

  @override
  Widget build(BuildContext context) {
    return AnimatedSwitcher(
      duration: const Duration(milliseconds: 200),
      transitionBuilder: (child, animation) {
        return FadeTransition(
          opacity: animation,
          child: child,
        );
      },
      child: Text(
        inferTagText(),
        key: ValueKey<String>(inferTagText()),
        style: TextStyle(
          color: ThemeX.textColor,
          fontFamily: "Ubuntu Mono",
          fontSize: 14,
          fontWeight: FontWeight.bold
        ),
      ),
    );
  }

}


