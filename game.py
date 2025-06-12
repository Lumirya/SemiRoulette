import random
from enum import Enum
from time import sleep
from termcolor import colored


class Item:
    class Item_Type(Enum):
        nothing = 0
        handcuff = 1
        knife = 2
        beer = 3
        magnifier = 4
        zhonghua = 5

    def __init__(self, item_type: Item_Type) -> None:
        self.item_type = item_type
        if item_type == self.Item_Type.nothing:
            assert False, "Cannot create an item with type nothing"
        if item_type == self.Item_Type.handcuff:
            self.name = "Handcuff"
            self.description = "Handcuff the next player, skip his turn"
        if item_type == self.Item_Type.knife:
            self.name = "Knife"
            self.description = "magnify the gun, double its damage of next shot"
        if item_type == self.Item_Type.beer:
            self.name = "Beer"
            self.description = "skip one bullet in the gun"
        if item_type == self.Item_Type.magnifier:
            self.name = "Magnifier"
            self.description = "show the next bullet in the gun"
        if item_type == self.Item_Type.zhonghua:
            self.name = "Zhonghua"
            self.description = "give you one more live"


class Player:
    class Player_Status(Enum):
        normal = 1
        handcuffed = 2
        handcuffed_but_ready_to_escape = 3

    def __init__(self, name: str, lives: int, item_num: int) -> None:
        self.name = name
        self.lives = lives
        self.item_num = item_num
        self.item_list = []

        self.status = self.Player_Status.normal

        if name == "Dealer":
            self.next_shoot_self = False
            self.next_bullet_live = False
            self.bullet_info_valid = False

    def __str__(self) -> str:
        print("Not implemented yet")
        return ""

    def get_lives(self) -> int:
        return self.lives

    def get_item_list(self) -> list:
        return self.item_list

    def display_item_list(self) -> None:
        print(f"{self.name}'s {colored('items', 'blue')}: ", end="")
        for item in self.item_list:
            print(colored(item.name, "yellow"), end=" ")
        if self.name != "Dealer":
            print(
                f"\nType the item {colored('name', 'blue')} to use it, type nothing to skip this part"
            )
        else:
            print("")


class Gun:
    def __init__(self, live_bullet: int, blank_bullet: int) -> None:
        # generate a list of bullets using live_bullet and blank_bullet
        self.bullets = [True] * live_bullet + [False] * blank_bullet
        # shuffle the list
        random.shuffle(self.bullets)

        self.knifed = False

    def get_next_bullet(self) -> bool:
        # return the first bullet in the list
        return self.bullets.pop(0)

    def show_next_bullet(self) -> bool:
        # return the first bullet in the list
        return self.bullets[0]

    def num_bullets(self) -> int:
        # return the number of bullets in the list
        return len(self.bullets)

    def knife(self) -> None:
        # magnify the gun
        self.knifed = True

    def count_live_bullets(self) -> int:
        # count the number of live bullets in the list
        return sum(self.bullets)

    def count_blank_bullets(self) -> int:
        # count the number of blank bullets in the list
        return len(self.bullets) - self.count_live_bullets()


class Game:
    def __init__(self) -> None:
        self.players = []
        self.next_player_id = 0
        pass

    def add_human_player(self, name: str, lives, item_num) -> None:
        self.players.append(Player(name, lives, item_num))

    def add_computer_player(self, lives, item_num) -> None:
        self.players.append(Player("Dealer", lives, item_num))

    def randomize_players(self) -> None:
        random.shuffle(self.players)
        print(f"Player {colored(self.players[0].name, 'yellow', 'on_blue')} goes first")

    def add_gun(self, live_bullet: int, blank_bullet: int) -> None:
        self.gun = Gun(live_bullet, blank_bullet)

    def pick_item(self, player_id: int) -> None:
        for _ in range(self.players[player_id].item_num):
            if len(self.players[player_id].item_list) >= 8:
                return
            item_type = random.randint(1, 5)
            self.players[player_id].item_list.append(Item(Item.Item_Type(item_type)))
            colored_player_name = colored(
                self.players[player_id].name, "yellow", "on_blue"
            )
            colored_item_name = colored(
                self.players[player_id].item_list[-1].name, "red"
            )
            print(f"Player {colored_player_name} picked up a {colored_item_name}")

    def computer_before_turn(self, player_id: int) -> bool:
        player_id = player_id
        return True

    def before_turn(self, player_id: int) -> bool:
        """_summary_

        1. check if the player is handcuffed

        Args:
            player_id (int): which player is playing using self.players[player_id]

        Returns:
            bool: True if continue to after_turn, False if the player is handcuffed
                skip this turn
        """

        self.print_seperator()
        # display each player's lives
        for i in range(len(self.players)):
            colored_player_name = colored(self.players[i].name, "yellow", "on_blue")
            print(
                "Player {} has {} lives".format(
                    colored_player_name, self.players[i].lives
                )
            )

        self.print_seperator()
        colored_player_name = colored(self.players[player_id].name, "yellow", "on_blue")
        print("Now it's player {}'s turn".format(colored_player_name))

        if self.players[player_id].status == Player.Player_Status.handcuffed:
            self.next_player_id = (player_id + 1) % len(self.players)
            print("{} is handcuffed, skip his turn".format(colored_player_name))
            self.players[
                player_id
            ].status = Player.Player_Status.handcuffed_but_ready_to_escape
            return False

        if (
            self.players[player_id].status
            == Player.Player_Status.handcuffed_but_ready_to_escape
        ):
            self.players[player_id].status = Player.Player_Status.normal
            print(
                "{} was handcuffed, but he can escape now".format(colored_player_name)
            )

        return True

    def print_seperator(self) -> None:
        print("=" * 80)

    def check_gun_blank_and_renew(self) -> None:
        if hasattr(self, "gun") and self.gun.num_bullets() != 0:
            return
        live = 5
        blank = 3
        self.gun = Gun(live, blank)
        colored_live = colored("live", "red")
        colored_blank = colored("blank", "green")
        print(
            f"The gun is reloaded with {live} {colored_live} bullets and {blank} {colored_blank} bullets"
        )
        for i in range(len(self.players)):
            self.pick_item(i)
        self.print_seperator()

    def player_using_item(self, player_id: int, item: Item.Item_Type) -> bool:
        colored_player_name = colored(self.players[player_id].name, "yellow", "on_blue")
        colored_next_player_name = colored(
            self.players[(player_id + 1) % len(self.players)].name, "yellow", "on_blue"
        )
        print(f"{colored_player_name} is using item: ", colored(item.name, "yellow"))
        if self.players[player_id].name == "Dealer":
            sleep(2)
        if item == Item.Item_Type.handcuff:
            if (
                self.players[(player_id + 1) % len(self.players)].status
                != Player.Player_Status.normal
            ):
                print(
                    f"Player {colored_next_player_name} is already handcuffed, you cannot handcuff him again"
                )
                return False
            self.players[
                (player_id + 1) % len(self.players)
            ].status = Player.Player_Status.handcuffed
            print(f"Player {colored_player_name} handcuffed the next player")
        if item == Item.Item_Type.knife:
            self.gun.knife()
            print(f"Player {colored_player_name} magnified the gun")

        if item == Item.Item_Type.beer:
            live = self.gun.get_next_bullet()
            colored_output = colored(
                "live" if live else "blank", "red" if live else "green"
            )
            print(f"Player {colored_player_name} skipped one bullet in the gun")
            print("The skipped bullet is: ", colored_output)
        if item == Item.Item_Type.magnifier:
            live = self.gun.show_next_bullet()
            colored_output = colored(
                "live" if live else "blank", "red" if live else "green"
            )
            print(f"Player {colored_player_name} showed the next bullet in the gun")
            print("The next bullet is: ", colored_output)
            if self.players[player_id].name == "Dealer":
                self.players[player_id].next_bullet_live = live
                self.players[player_id].bullet_info_valid = True

        if item == Item.Item_Type.zhonghua:
            if self.players[player_id].lives >= 6:
                print(
                    f"Player {colored_player_name} already has 6 lives, cannot get more"
                )
                return False
            self.players[player_id].lives += 1
            print(f"Player {colored_player_name} got one more live")
            print(
                f"Now {colored_player_name} has {self.players[player_id].lives} lives"
            )

        return True

    def computer_choose_item(self, player_id: int) -> Item.Item_Type:
        if self.players[player_id].name != "Dealer":
            assert False, "This function is only for computer player"
        player = self.players[player_id]
        print("Dealer is thinking...")
        sleep(2)

        next_player_id = (player_id + 1) % len(self.players)
        next_player = self.players[next_player_id]

        def check_if_has_item(item_type: Item.Item_Type) -> bool:
            for item in self.players[player_id].item_list:
                if item.item_type == item_type:
                    return True
            return False

        live_count = self.gun.count_live_bullets()
        blank_count = self.gun.count_blank_bullets()
        if not live_count:
            player.next_shoot_self = True
            return Item.Item_Type.nothing

        if not blank_count:
            if check_if_has_item(Item.Item_Type.knife) and not self.gun.knifed:
                return Item.Item_Type.knife
            player.next_shoot_self = False
            return Item.Item_Type.nothing

        if check_if_has_item(Item.Item_Type.zhonghua) and player.lives < 6:
            return Item.Item_Type.zhonghua

        if check_if_has_item(Item.Item_Type.magnifier) and not player.bullet_info_valid:
            return Item.Item_Type.magnifier

        if (
            check_if_has_item(Item.Item_Type.handcuff)
            and next_player.status == Player.Player_Status.normal
        ):
            return Item.Item_Type.handcuff

        if player.bullet_info_valid:
            if player.next_bullet_live:
                if check_if_has_item(Item.Item_Type.knife) and not self.gun.knifed:
                    return Item.Item_Type.knife
                player.next_shoot_self = False
                return Item.Item_Type.nothing
            else:
                player.next_shoot_self = True
                return Item.Item_Type.nothing

        if check_if_has_item(Item.Item_Type.beer) and (
            blank_count == 1 or live_count == 1
        ):
            return Item.Item_Type.beer

        if blank_count > live_count:
            player.next_shoot_self = True
            return Item.Item_Type.nothing
        else:
            player.next_shoot_self = False
            return Item.Item_Type.nothing

    def process_item_info(self, player_id: int) -> Item.Item_Type:
        if self.players[player_id].name == "Dealer":
            item_name = self.computer_choose_item(player_id)
            self.players[player_id].display_item_list()
            item_name = item_name.name.lower()
        else:
            self.players[player_id].display_item_list()
            item_name = input().strip().replace("\r", "").replace("\n", "").lower()
        if not item_name:
            return Item.Item_Type.nothing
        for item in self.players[player_id].get_item_list():
            if item.name.lower() == item_name or item_name in item.name.lower():
                rst = self.player_using_item(player_id, item.item_type)
                if rst:
                    self.players[player_id].get_item_list().remove(item)
                return item.item_type
        return Item.Item_Type.nothing

    def process_shoot(self, player_id: int) -> bool:
        next_player_id = (player_id + 1) % len(self.players)
        colored_next_player_name = colored(self.players[next_player_id].name, "red")
        if self.players[player_id].name == "Dealer":
            self.players[player_id].bullet_info_valid = False
            if self.players[player_id].next_shoot_self:
                print("Dealer chooses to shoot himself")
                return True
            else:
                print(f"Dealer chooses to shoot {colored_next_player_name}")
                return False
        print(
            f"Choose where to shoot: (1) {colored('yourself', 'green')} (2) {colored_next_player_name}"
        )
        try:
            rst = int(input().strip().replace("\r", "").replace("\n", ""))
            assert rst in [1, 2]
            if rst == 1:
                return True
            if rst == 2:
                return False
        except Exception as _:
            print("Wrong input, please try again")
            return self.process_shoot(player_id)
        return False

    def after_turn(self, player_id: int, choose_self: bool) -> None:
        # choose_self: True if the player choose to shoot himself
        if choose_self:
            live = self.gun.get_next_bullet()
            colored_live = colored("live", "red") if live else colored("blank", "green")
            next_player_id = (player_id + 1) % len(self.players)
            colored_next_player_name = colored(
                self.players[next_player_id].name, "yellow", "on_blue"
            )
            colored_player_name = colored(
                self.players[player_id].name, "yellow", "on_blue"
            )
            player_name = self.players[player_id].name
            print(f"{colored_player_name} chooses to shoot himself")
            if live:
                dmg = 2 if self.gun.knifed else 1
                self.players[player_id].lives -= dmg
                self.next_player_id = (player_id + 1) % len(self.players)
                warn_msg = colored(f"{player_name} is SHOT", "red", "on_white")
                print(warn_msg)
                print(f"{colored_player_name} has been shot. He loses {dmg} lives")
                if self.players[player_id].lives > 0:
                    print(
                        f"Now {colored_player_name} has {self.players[player_id].lives} lives"
                    )

            if not live:
                warn_msg = colored("IT WAS LUCKY", "green", "on_blue")
                print(warn_msg)
                print(f"No one is hurt, the bullet is {colored_live}")

        else:
            live = self.gun.get_next_bullet()
            next_player_id = (player_id + 1) % len(self.players)
            colored_live = colored("live", "red") if live else colored("blank", "green")
            colored_next_player_name = colored(
                self.players[next_player_id].name, "yellow", "on_blue"
            )
            colored_player_name = colored(
                self.players[player_id].name, "yellow", "on_blue"
            )
            next_player_name = self.players[next_player_id].name
            print(f"{colored_player_name} chooses to shoot {colored_next_player_name}")

            if live:
                dmg = 2 if self.gun.knifed else 1
                self.players[next_player_id].lives -= dmg
                warn_msg = colored(f"{next_player_name} IS SHOT", "red", "on_white")
                print(warn_msg)
                print(
                    f"player {colored_player_name} shoot the next player {colored_next_player_name}, {colored_next_player_name} loses {dmg} lives"
                )
                if self.players[next_player_id].lives > 0:
                    print(
                        f"Now {colored_next_player_name} has {self.players[next_player_id].lives} lives"
                    )

                self.next_player_id = next_player_id

            if not live:
                warn_msg = colored(" IT WAS LUCKY", "green", "on_blue")
                print(warn_msg)
                print(f"No one is hurt. The bullet is {colored_live}")
                self.next_player_id = next_player_id
        if self.gun.knifed:
            print("The gun is no longer magnified")
        self.gun.knifed = False

    def easy_game_loop(self) -> None:
        while True:
            self.check_gun_blank_and_renew()
            if not self.before_turn(self.next_player_id):
                continue
            while self.process_item_info(self.next_player_id) != Item.Item_Type.nothing:
                self.check_gun_blank_and_renew()
                continue

            choose_self = self.process_shoot(self.next_player_id)
            self.after_turn(self.next_player_id, choose_self)
            for player in self.players:
                if player.get_lives() <= 0:
                    self.game_over()
                    return

    def game_over(self) -> None:
        for player in self.players:
            if player.get_lives() > 0:
                colored_player_name = colored(player.name, "yellow", "on_blue")
                print(f"Player {colored_player_name} wins!")


def thanks():
    print("Thanks for playing!")


if __name__ == "__main__":
    game = Game()
    game.add_human_player("Alice", 6, 4)
    # game.add_human_player("Bob", 6, 4)
    game.add_computer_player(6, 4)
    game.randomize_players()
    game.check_gun_blank_and_renew()
    game.easy_game_loop()

    thanks()
