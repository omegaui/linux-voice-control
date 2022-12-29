

import 'package:flutter/material.dart';
import 'package:lvc_gui_flutter/main.dart';

import '../themex.dart';

class StatusIndicator extends StatelessWidget{
  const StatusIndicator({super.key});

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
        status,
        key: ValueKey<String>(status),
        style: TextStyle(
            color: ThemeX.textColor,
            fontFamily: "Ubuntu Mono",
            fontSize: 14,
        ),
      ),
    );
  }

}



