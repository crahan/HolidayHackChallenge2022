# Welcome

![Title Image](./img/misc/title_image.png)


## Introduction

![OMG! Let's go!!!](./img/misc/lets_go.gif){ align=left } Hello there and welcome to my [2022 SANS Holiday Hack Challenge](https://holidayhackchallenge.com/2022/) write-up. Here we are again, for the fifth time no less. In 2020, my write-up won best technical answer. In 2021, I was extremely fortunate to win first prize. This year, more than ever, my motivation is you. The first time player, the cybersecurity enthousiast, the seasoned professional, and every role in between. May this write-up provide you with that nudge to help solve that final challenge or be a learning guide as you dip your toes in the exciting world of cybersecurity! :hugging_face:

Similar to previous years, there's 3 main sections. This page which contains the introduction, answers, the overall narrative, and final conclusion. [Objectives](./objectives/o1.md) contains the write-ups for the main objectives for which an answer had to be submitted and [Terminal Hints](./hints/h2.md) has the write-ups for the additional side challenges which provide you with hints to help solve the main objectives.

As always, there's a few things worth highlighting like [insert list of interesting challenges, solutions, and hacks], the very incomplete list of [Easter eggs](./easter_eggs.md), and all of the [custom scripts](https://github.com/crahan/HolidayHackChallenge2022/tree/main/docs/tools) used throughout the game.

!!! note "50-page submission limit"
    Each year there's a huge number of write-ups that need to be reviewed by the SANS and Counter Hack teams. To find a good middle ground between preventing information overload and creating a write-up that can stand on its own as a learning resource, some parts, like the *navigation tip* below, are collapsed by default. Skipping over these will not take away from understanding the overall solution, but feel free to expand them to get some additional information.

??? tip "Navigation tip"
    Even with less than 50 pages, there's still quite a bit of information to read through. To make things a little easier, you can use ++"P"++ or ++","++ to go to the previous section, ++"N"++ or ++"."++ to navigate to the next section, and ++"S"++, ++"F"++, or ++"/"++ to open up the search dialog.

    **TL;DR** if you keep pressing ++"N"++ or ++"."++ from this point forward, you'll hit all the content in the right order! :smile:


## Answers

!!! done "1. KringleCon Orientation - :fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    Follow [Jingle Ringford's instructions](./objectives/o2.md) to open the gate.

!!! done "2. Wireshark Practice - :fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    [Answer to Objective 2](./objectives/o2.md)

!!! done "3. Windows Event Logs - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    [Answer to Objective 3](./objectives/o3.md)

!!! done "4. Suricata Regatta - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star:"
    [Answer to Objective 4](./objectives/o4.md)

!!! done "5. Clone with a Difference - :fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    [`maintainers`](./objectives/o5.md)

!!! done "6. Prison Escape - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star:"
    [`082bb339ec19de4935867`](./objectives/o6.md)

!!! done "7. Jolly CI/CD - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star:"
    [`oI40zIuCcN8c3MhKgQjOMN8lfYtVqcK`](./objectives/o7.md)

!!! done "8. Boria PCAP Mining - :fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    [`http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance`](./objectives/o8.md)

!!! done "9. Open Boria Mine Door - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    [Answer to Objective 9](./objectives/o9.md)

!!! done "10. Glamtariel's Fountain - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star:"
    [`goldring-morethansupertopsecret76394734.png`](./objectives/o10.md)

!!! done "11. AWS CLI Intro1 - :fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    [Answer to Objective 11](./objectives/o11.md)

!!! done "12. Trufflehog Search - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    [`put_policy.py`](./objectives/o12.md)

!!! done "13. Exploitation via AWS CLI - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star:"
    [Answer to Objective 13](./objectives/o13.md)

!!! done "14. Buy a Hat - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star::fontawesome-regular-star::fontawesome-regular-star:"
    [Answer to Objective 14](./objectives/o14.md)

!!! done "15. Blockchain Divination - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-regular-star:"
    [`0xc27A2D3DE339Ce353c0eFBa32e948a88F1C86554`](./objectives/o15.md)

!!! done "16. Exploit a Smart Contract - :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star:"
    [Answer to Objective 16](./objectives/o16.md)


## NPC locations

| :material-account: Name | :material-map-marker: Area | :material-gamepad: Challenge                  |
| :---------------------- | :------------------------: | :-------------------------------------------- |
| Jingle RingFord         |          Staging           | [KringleCon Orientation](objectives/o1.md)    |
| Chimney Scissorsticks   |          Approach          | -                                             |
| Santa                   |          Approach          | -                                             |
| Garland Candlesticks    |          Netwars           | -                                             |
| Grinchum                |       Underground #1       | -                                             |
| Morcel Nougat           |       Underground #1       | -                                             |
| Tangle Coalbox          |       Underground #1       | -                                             |
| Sparkle Redberry        |        Tolkien Ring        | [Wireshark Practice](objectives/o2.md)        |
| Dusty Giftwrap          |        Tolkien Ring        | [Windows Event Logs](objectives/o3.md)        |
| Fitzy Shortstack        |        Tolkien Ring        | [Suricata Regatta](objectives/o4.md)          |
| Brozeek                 |       Underground #1       | -                                             |
| Crozag                  |       Underground #1       | -                                             |
| Bow Ninecandle          |         Elfen Ring         | [Clone with a Difference](objectives/o5.md)   |
| Tinsel Upatree          |         Elf House          | [Prison Escape](objectives/o6.md)             |
| Rippin Proudboot        |         Elf House          | [Jolly CI/CD](objectives/o7.md)               |
| Alabaster Snowball      |          Web Ring          | [Boria PCAP Mining](objectives/o8.md)         |
| Hal Tandybuck           |          Web Ring          | [Open Boria Mind Door](objectives/o9.md)      |
| Akbowl                  |          Fountain          | [Glamtariel's Fountain](objectives/o10.md)    |
| Jill Underpole          |         Cloud Ring         | [AWS CLI Intro](objectives/o11.md)            |
| Gerty Snowburrow        |         Cloud Ring         | [Trufflehog Search](objectives/o12.md)        |
| Sulfrod                 |         Cloud Ring         | [Exploitation via AWS CLI](objectives/o13.md) |
| Wombley Cube            |    Burning Ring of Fire    | [Buy a Hat](objectives/o14.md)                |
| Palzari                 |    Burning Ring of Fire    | [Buy a Hat](objectives/o14.md)                |
| Chorizo                 |    Burning Ring of Fire    | -                                             |
| Slicmer                 |    Burning Ring of Fire    | [Blockchain Divination](objectives/o15.md)    |
| Luigi                   |    Burning Ring of Fire    | [Exploit a Smart Contract](objectives/o16.md) |
| Santa                   |           Entry            | -                                             |
| Rose Mold               |           Entry            | -                                             |
| Timpy Toque             |           Entry            | -                                             |
| Eve Snowshoes           |           Entry            | -                                             |
| Smilegol                |           Entry            | -                                             |
| Angel Candysalt         |           Entry            | -                                             |


## Conclusion

??? Abstract "Narrative"
    Five Rings for the Christmas king immersed in cold<br>
    Each Ring now missing from its zone<br>
    The first with bread kindly given, not sold<br>
    Another to find 'ere pipelines get owned<br>
    One beneath a fountain where water flowed<br>
    Into clouds Grinchum had the fourth thrown<br>
    The fifth on blockchains where shadows be bold<br>
    One hunt to seek them all, five quests to find them<br>
    One player to bring them all, and Santa Claus to bind them

![Group photo](./img/misc/castle_entry.png)

!!! quote "Santa"
    Congratulations! You have foiled Grinchum's foul plan and recovered the Golden Rings!<br/>
    And by the magic of the rings, Grinchum has been restored back to his true, merry self: Smilegol!<br/>
    You see, all Flobbits are drawn to the Rings, but somehow, Smilegol was able to snatch them from my castle.<br/>
    To anyone but me, their allure becomes irresistable the more Rings someone possesses.<br/>
    That allure eventually tarnishes the holder's Holiday Spirit, which is about giving, not possesing.<br/>
    That's exactly what happened to Smilegol; that selfishness morphed him into Grinchum.<br/>
    But thanks to you, Grinchum is no more, and the holiday season is saved!<br/>
    Ho ho ho, happy holidays!

!!! quote "Rose Mold"
    I'm Rose Mold. What planet are you from?<br/>
    What am I doing here? I could ask the same of you!<br/>
    Collecting web, cloud, elfen rings... What about onion rings? A Sebring?<br/>
    n00bs...

!!! quote "Timpy Toque"
    Thank you for saving Smilegol and protecting the Rings.<br/>
    You will always be a friend of the Flobbits.

!!! quote "Eve Snowshoes"
    Hello there, super helper! I'm Eve Snowshoes.<br/>
    The other elves and I are so glad you were able to help recover the rings!<br/>
    The holidays wouldn't have been the same without your hard work.<br/>
    If you'd like, you can order special swag that's only available to our victors!<br/>
    Thank you!

!!! quote "Smilegol"
    I must give you my most thankful of thanks, and most sorry of sorries.<br/>
    I'm not sure what happened, but I just couldn't resist the Rings' call.<br/>
    But once you returned the Rings to Santa, I was no longer so spellbound.<br/>
    I could think clearly again, so I shouted off that awful persona.<br/>
    And that grouchy Grinchum was gone for good. Now, I can be me again, just in time for gift giving.<br/>
    This is a lesson I won't soon forget, and I certainly won't forget you.<br/>
    I wish you smooth sailing on wherever your next voyage takes you!

!!! quote "Angel Candysalt"
    Greetings North Pole savior! I'm Angel Candysalt!<br/>
    A euphemism? No, that's my name. Why are people still asking me that?<br/>
    Anywho, thank you for everything you've done.<br/>
    You'll go down in history!
