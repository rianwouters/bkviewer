from .action import Action


class SimpleWitnessPrinter(Action):
    def witness(self, w):
        print(f'{w.person.fullname} #{w.person.id}')
