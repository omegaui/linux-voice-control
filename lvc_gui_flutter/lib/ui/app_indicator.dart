
import 'package:flutter/material.dart';
import 'package:lvc_gui_flutter/constantsx.dart';
import 'package:lvc_gui_flutter/main.dart';

class AppIndicator extends StatelessWidget{
  const AppIndicator({super.key});

  @override
  Widget build(BuildContext context) {
    bool listening = tag == ConstantsX.listeningTag;
    bool sleeping = tag == ConstantsX.sleepingTag;
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      width: !listening && !sleeping ? 24 : 30,
      height: !listening && !sleeping ? 24 : 30,
      decoration: BoxDecoration(
        color: inferTagColor(),
        borderRadius: BorderRadius.circular(listening || sleeping ? 10 : 40),
      ),
      child: Center(
        child: AnimatedSwitcher(
          duration: const Duration(milliseconds: 200),
          transitionBuilder: (child, animation) => FadeTransition(opacity: animation, child: child),
          child: listening ? Container(
            key: const Key('box2'),
            width: 20,
            height: 20,
            decoration: BoxDecoration(
              color: Colors.green,
              borderRadius: BorderRadius.circular(10),
            ),
          ) : Container(
            key: const Key('box'),
            width: 18,
            height: 18,
            decoration: BoxDecoration(
              color: sleeping ? Colors.blue.shade600 : Colors.grey.shade300,
              borderRadius: BorderRadius.circular(sleeping ? 10 : 20),
            ),
          ),
        ),
      ),
    );
  }

}



