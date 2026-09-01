# Flutter Widget-Test Recipes

Load this reference only when the selected interaction needs it.

## Pump and Interact Deliberately

- Static render: `pumpWidget`, then assert.
- One synchronous state change: trigger it, then use `pump()`.
- Text input: `enterText`, trigger the action that consumes it, then pump.
- A long list: use `scrollUntilVisible` with the intended scrollable before
  interacting with the item.
- A finite animation or known async completion: use `pumpAndSettle()`. Do not
  use it for an indefinitely scheduled animation, timer, or stream; pump a
  bounded duration or expose a deterministic seam instead.

## Compact Interaction Example

```dart
testWidgets('adds then removes a todo', (tester) async {
  await tester.pumpWidget(const TodoList());
  expect(find.byType(ListTile), findsNothing);

  await tester.enterText(find.byType(TextField), 'Buy groceries');
  await tester.tap(find.byType(FloatingActionButton));
  await tester.pump();
  expect(find.text('Buy groceries'), findsOneWidget);

  await tester.drag(find.byType(Dismissible), const Offset(500, 0));
  await tester.pumpAndSettle();
  expect(find.text('Buy groceries'), findsNothing);
});
```

Use a key, semantic label, or callback seam when visible text is not a stable
public contract. The test target should remain the observable behavior, not the
particular internal widget tree.
