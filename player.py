# file: player.py
from py4godot.classes import gdclass
from py4godot.classes.Area2D import Area2D
from py4godot.classes.core import Vector2
from py4godot.classes.AnimatedSprite2D import AnimatedSprite2D
from py4godot.classes.CollisionShape2D import CollisionShape2D
from py4godot.signals import signal
from py4godot.utils.utils import get_viewport
from py4godot.classes.Input import Input


@gdclass
class player(Area2D):
    # Signals
    hit = signal([])

    # Exported-like properties (shown in the Inspector)
    speed: float = 400.0
    screen_size: Vector2 = Vector2.new2(0, 0)

    def _ready(self) -> None:
        print("ready")
        viewport = get_viewport(self)
        # Same as get_viewport().get_visible_rect().size in GDScript
        self.screen_size = viewport.get_visible_rect().size

    def _process(self, delta: float) -> None:
        input_inst: Input = Input.get_instance()

        velocity = Vector2.new2(0, 0)
        if input_inst.is_action_pressed("move_right"):
            velocity.x += 1
        if input_inst.is_action_pressed("move_left"):
            velocity.x -= 1
        if input_inst.is_action_pressed("move_down"):
            velocity.y += 1
        if input_inst.is_action_pressed("move_up"):
            velocity.y -= 1

        sprite: AnimatedSprite2D = self.get_node("AnimatedSprite2D")

        if velocity.length() > 0:
            velocity = velocity.normalized() * self.speed
            sprite.play()
        else:
            sprite.stop()

        self.position = self.position + velocity * delta
        self.position = self.position.clamp(Vector2.new2(0, 0), self.screen_size)

        if velocity.x != 0:
            sprite.animation = "walk"
            sprite.flip_v = False
            sprite.flip_h = (velocity.x < 0)
        elif velocity.y != 0:
            sprite.animation = "up"
            sprite.flip_v = (velocity.y > 0)

    # Connect Area2D's "body_entered" to this from the editor or in code
    def _on_body_entered(self, body) -> None:
        self.hide()
        self.hit.emit()
        col: CollisionShape2D = self.get_node("CollisionShape2D")
        col.set_deferred("disabled", True)

    def start(self, pos: Vector2) -> None:
        self.position = pos
        self.show()
        col: CollisionShape2D = self.get_node("CollisionShape2D")
        # enabling immediately is fine outside physics callback
        col.disabled = False

