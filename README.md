# Description
In that project I try to build model, which can define cuts in video.


# Data Sources
I've downloaded videos from Youtube and cut them by Kdenlive.

|  | file | clip name | youtube link |
| --- | --- | --- | --- |
| 0 | videos/0.mp4 | Rammstein - Du Hast | https://www.youtube.com/watch?v=W3q8Od5qJio |
| 1 | videos/1.mp4 | Rammstein - Rosenrot | https://www.youtube.com/watch?v=af59U2BRRAU |
| 2 | videos/2.mp4 | Rammstein - Sonne | https://www.youtube.com/watch?v=StZcUAPRRac |
| 3 | videos/3.mp4 | Замай - Одинокое Пламя | https://www.youtube.com/watch?v=jn9pwdmKpXU |
| 4 | videos/4.mp4 | SKRILLEX - Bangarang feat. Sirah | https://www.youtube.com/watch?v=YJVmu6yttiw |
| 5 | videos/5.mp4 | IC3PEAK - Плак-Плак | https://www.youtube.com/watch?v=Y6tDdjOmsCY |


There are disolve and dip to white/black transitions in source videos. I don't label the first as cut, but for the second that's possible to see where exactly shot changes, so I labeled them as cuts almost accurate.

The example of cut with dip to black transition you can see in `pics/dipToBlack_cuts0.png`.

## How I managed this data
There are 3 Rammstein clips, which contain a lot of actions, like fires, explosions, flashs or just jerks. I used 2 of them to learn and validate. Then checked the model with the 3rd. And I got many false positive results.

So I checked how the model predict cuts on less agressive video, and tool the video of an another artist. And yes, the model predicts cuts of more peacefull videos a little better.
