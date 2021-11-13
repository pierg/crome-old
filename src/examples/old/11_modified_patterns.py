from core.type import Boolean

p1 = Boolean("p1")
p2 = Boolean("p2")
a = Boolean("a")
c = Boolean("c")


def modified():
    from core.specification.atom.pattern.robotics.trigger.triggers_modified import (
        BoundDelay,
        BoundReaction,
        DelayedReaction,
        InstantaneousReaction,
        PromptReaction,
        Wait,
    )

    original_patterns = []
    original_patterns.append(
        InstantaneousReaction(pre=p1, post=p2, active=a, context=c)
    )
    original_patterns.append(PromptReaction(pre=p1, post=p2, active=a, context=c))
    original_patterns.append(DelayedReaction(pre=p1, post=p2, active=a, context=c))
    original_patterns.append(BoundReaction(pre=p1, post=p2, active=a, context=c))
    original_patterns.append(BoundDelay(pre=p1, post=p2, active=a, context=c))
    original_patterns.append(Wait(pre=p1, post=p2, active=a, context=c))
    return original_patterns


def original():
    from core.specification.atom.pattern.robotics.trigger.triggers import (
        BoundDelay,
        BoundReaction,
        DelayedReaction,
        InstantaneousReaction,
        PromptReaction,
        Wait,
    )

    modified_patterns = []
    modified_patterns.append(InstantaneousReaction(pre=p1, post=p2))
    modified_patterns.append(PromptReaction(pre=p1, post=p2))
    modified_patterns.append(DelayedReaction(pre=p1, post=p2))
    modified_patterns.append(BoundReaction(pre=p1, post=p2))
    modified_patterns.append(BoundDelay(pre=p1, post=p2))
    modified_patterns.append(Wait(pre=p1, post=p2))
    return modified_patterns


if __name__ == "__main__":
    original = original()
    modified = modified()

    for i, o in enumerate(original):

        print(f"\n\nORIGINAL\t{o}")
        m = modified[i]
        print(f"MODIFIED\t{m}")
        print(f"ORIGINAL REFINES MODIFIED \t{o <= m}")
        print(f"MODIFIED REFINES ORIGINAL \t{m <= o}")
