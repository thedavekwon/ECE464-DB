from re import sub
import mongomock
import pytest

from src.client import RedditClient


@pytest.fixture(scope="session")
def rc():
    db = mongomock.MongoClient().reddit
    
    # Test data
    submissions = [
        {
            "author": {"_id": "1w72", "name": "spez"},
            "comments": [
                {
                    "_id": "g4k3btr",
                    "body": "Help facilitate better discussions of Reddit announcements. [Crosspost this post to a relevant community](https://www.reddit.com/submit/?url=https%3A%2F%2Fwww.reddit.com%2Fr%2Fannouncements%2Fcomments%2Fipitt0%2Ftoday_were_testing_a_new_way_to_discuss_political%2F&title=Today%20we%E2%80%99re%20testing%20a%20new%20way%20to%20discuss%20political%20ads%20%28and%20announcements%29) to ask questions and start a discussion.\n\n* r/TagPro - [Discuss Spez's post (or don't) with TagPro, a free online capture the flag game with a thriving Reddit community!](/comments/ippnca) (107 upvotes, 81 comments)  \n* r/foundthemobileuser - [I just want this to appear on the stickied comments. Follow u/darknep!](/comments/ipo6ut) (0 upvotes, 5 comments)  \n* r/csgo - [Relevant schmelevant](/comments/ipnvwc) (23 upvotes, 8 comments)  \n* r/lincoln - [Reddit is rolling out a new political ads discussion platform. Mods please recognize the need for this in our community.](/comments/ipnlx7) (0 upvotes, 18 comments)  \n* r/neoliberal - [Today we’re testing a new way to discuss political ads (and announcements) - reddit](/comments/ipmu6q) (6 upvotes, 9 comments)  \n* r/test - [Test to see if this crosspost will appear in the stickied comment or be removed](/comments/ipl09c) (39 upvotes, 46 comments)  \n* r/donaldtrump - [Today we’re testing a new way to discuss political ads (and announcements)](/comments/ipk9nm) (0 upvotes, 58 comments)  \n* r/JoeBiden - [Reddit are testing a new way to discuss political ads (and announcements)](/comments/ipk1dt) (43 upvotes, 39 comments)  \n* r/OnionLovers - [Spez made a post to r/announcements and forgot to mention his favorite food - ONIONS](/comments/ipjw96) (136 upvotes, 29 comments)  \n* r/AgainstHateSubreddits - [After previously announcing that Reddit would be selling a Trump homepage takeover on Reddit, today Steve \"spez\" Huffman states Reddit will not allow any comments on political ads](/comments/ipjm8d) (395 upvotes, 81 comments)  \n* r/ideasfortheadmins - [Admins are testing a new announcement feature to redirect discussion to different communities - Feel free to comment with your ideas for that feature here](/comments/ipjfsv) (2 upvotes, 41 comments)  \n* r/LincolnProject - [Reddit site wide FYI - Today we’re testing a new way to discuss political ads (and announcements)](/comments/ipj5ll) (0 upvotes, 9 comments)  \n* r/SubredditDrama - [Spez makes an announcement in announcements locking announcements, guess he doesn't to hear about where the next T_D is growing](/comments/ipiwyi) (1209 upvotes, 712 comments)  \n* r/modnews - [Today we’re testing a new way to discuss political ads (and announcements)](/comments/ipiung) (0 upvotes, 1434 comments)  ",
                    "created_utc": 1599667595,
                    "author": {"_id": "6l4z3", "name": "AutoModerator"},
                    "score": 1,
                },
                {
                    "_id": "g4k4ckk",
                    "body": "Here are my responses from questions in various threads:\n\n* [Indeed. We did it this way because it was faster. If this approach works, we'll do a proper version with crossposts.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4k49hl/?utm_source=reddit&utm_medium=web2x&context=3)\n* [Yes,  you could already crosspost these threads. The change here is that 1)  we are encouraging communities to do so and 2) bringing those posts into  one place under the original post. The discussion posts would be  moderated within that community should they want to do so, but they  don’t have to, of course...](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4k5sjr/?utm_source=reddit&utm_medium=web2x&context=3)\n* [Just give it some time.](https://www.reddit.com/r/SubredditDrama/comments/ipiwyi/spez_makes_an_announcement_in_announcements/g4k45k4/?utm_source=reddit&utm_medium=web2x&context=3)\n* [The status quo was that Reddit would either moderate these discussions, or there would be no moderation at all, and I don’t think it’s appropriate for me to moderate either political discussions or criticism of me.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4k7ayq/?utm_source=reddit&utm_medium=web2x&context=3)\n* [We considered not having the ads at all, but I think that would be a  missed opportunity as ads (unfortunately) are a significant part of our  political process. They’re how candidates and issues reach voters they  may not otherwise be able to. We’ve seen other platforms ban such ads  completely or allow unfettered access, and we believe there must be a  better way.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4k8z53/?utm_source=reddit&utm_medium=web2x&context=3)\n* [Remember this isn’t just about r/announcements.  It’s really a test of how we encourage broad discussion of highly  visible posts that transcend a single community, in this case,  front-page political ads (and hopefully more).](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4kd45b/?utm_source=reddit&utm_medium=web2x&context=3)\n* [The reason we did the sticky comment approach was simply because it was  faster to build and it worked out of the box on every Reddit client,  including third-party apps. The political season is upon us, which means  time is tight, and this was a relatively new idea for how to address  moderation on political ads.](https://www.reddit.com/r/ideasfortheadmins/comments/ipjfsv/admins_are_testing_a_new_announcement_feature_to/g4kgjew/?utm_source=reddit&utm_medium=web2x&context=3)\n* [Proper crossposts work for r/announcements, but they don't show for ads because ads can't be crossposted (yet).](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4khwmt/?utm_source=reddit&utm_medium=web2x&context=3)\n* [Comments within the context of a community where there’s some culture  and norms around up and downvoting lead to better quality discussion.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4kj49n/?utm_source=reddit&utm_medium=web2x&context=3)\n* [I get your concern. In theory, us moderating a discussion critical of us  is similarly problematic. The posts are presently filtered through our  ads allow-list, which I think is appropriate for ads, but I’m open to a  different approach for r/announcements.](https://www.reddit.com/r/ideasfortheadmins/comments/ipjfsv/admins_are_testing_a_new_announcement_feature_to/g4kkzfu/?utm_source=reddit&utm_medium=web2x&context=3)\n* [Totally agree. We started with simple to try out the mechanic itself,  but there is plenty of opportunity to make this better and easier to  follow.](https://www.reddit.com/r/ideasfortheadmins/comments/ipjfsv/admins_are_testing_a_new_announcement_feature_to/g4klncz/?utm_source=reddit&utm_medium=web2x&context=3)\n* [The ads will show up wherever they are targeted, which for political ads  is fairly restricted. You can see all political ads and their targeting  on r/RedditPoliticalAds.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4knjwk/?utm_source=reddit&utm_medium=web2x&context=3)\n* [The discussions are just posts, so they’ll appear in any community where  a user submits it (as long as the mods and rules of that community  allow for it). The ads themselves will link to these discussion posts  instead of having direct comments specifically to address the challenge  of either a campaign or Reddit itself moderating political discussions  and as a way to encourage discussions within the context of a community.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4koiv1/?utm_source=reddit&utm_medium=web2x&context=3)\n* [Aside from the first few minutes we were live, AutoMod pulls posts from  communities on our ads allow-list that are not nsfw or private. (There  is also the same word filter we use for ads, which catches posts like  the other one you made here.)](https://www.reddit.com/r/test/comments/ipl09c/test_to_see_if_this_crosspost_will_appear_in_the/g4kpwgh/?utm_source=reddit&utm_medium=web2x&context=3)\n* [The reality is that we do not have a cohesive community in r/announcements,  nor is there a community around any particular ad, and a cohesive  community is a prerequisite for discussion. So, if we are to have any  discussion at all, it must be within a community.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4l3gto/?utm_source=reddit&utm_medium=web2x&context=3)\n* [I think one of the best missing features right now is multiple OPs. Would make group AMAs much easier.](https://www.reddit.com/r/ideasfortheadmins/comments/ipjfsv/admins_are_testing_a_new_announcement_feature_to/g4l3src/?utm_source=reddit&utm_medium=web2x&context=3)\n* [The status quo would have been the loudest political view would dominate  the conversation on any particular ad. With the approach we’re testing  today, we’ll see what different communities with different viewpoints  think. That’s the goal at least.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4l7k68/?utm_source=reddit&utm_medium=web2x&context=3)\n* [We may just disagree on this point. It certainly used to be the case  that there was a single Reddit community, and not just the time before  subreddits. However, Reddit has grown so much that that is no longer the  case. To many (millions) people, Reddit is just the subreddit they  spend the most time on rather than a monolith on its own. For better or  worse, Reddit has grown from a single community to a vast network of  communities.](https://www.reddit.com/r/modnews/comments/ipiung/today_were_testing_a_new_way_to_discuss_political/g4lb2e2/?utm_source=reddit&utm_medium=web2x&context=3)",
                    "created_utc": 1599668105,
                    "author": {"_id": "1w72", "name": "spez"},
                    "score": -5190,
                },
            ],
            "created_utc": 1599667576,
            "name": "t3_ipitt0",
            "score": 15548,
            "selftext": "In case you missed [the](https://www.reddit.com/r/mildlyinteresting/comments/ikxsst/this_reddit_billboard_advertisement_for_their/) [billboards](https://www.reddit.com/r/pics/comments/ilhck2/saw_one_in_the_wild_make_sure_to_vote_illinois/), [blog posts](https://redditblog.com/2020/09/01/its-national-poll-worker-recruitment-day-become-a-poll-worker-this-election-and-help-power-the-polls-in-your-community/), and [AMAs](https://redditblog.com/2020/08/25/voting-in-america/), we’re doing our best to encourage people on and off Reddit to vote this year. Along with our [Up the Vote campaign](https://redditblog.com/2020/07/29/up-the-vote-reddits-irl-2020-voting-campaign/) and [ongoing security and safety work](https://www.reddit.com/r/redditsecurity/) to guard against shenanigans, we’ve also been evolving how we handle another important aspect of the election process: **political ads**.\n\n## First, some background\n\nPolitical ads have been a relatively quiet part of Reddit for many years. Last year, in thinking through what the right balance was between unfettered political ads and prohibiting them altogether for 2020 (both approaches that other platforms have taken), we decided on [a policy we felt was the best approach for Reddit](https://www.reddit.com/r/announcements/comments/g0s6tn/changes_to_reddits_political_ads_policy/): no misinformation, human review of the ads and where they link, a subreddit listing all political ads ([r/RedditPoliticalAds](https://www.reddit.com/r/RedditPoliticalAds/)), and a requirement to keep comments on for 24 hours.\n\nSince debuting this policy earlier this year, the last condition (requiring comments to remain on) has enabled redditors to discuss political ads—providing more context in the comments and even offering counterarguments—but so far it’s only been lightly used. As we get closer to November, however, the prominence of and discussion around political ads will increase, and, with it, the need for a clear moderation system for these comments.\n\n## The problem we’re addressing\n\nAs I mentioned [a couple months back](https://www.reddit.com/r/announcements/comments/hi3oht/update_to_our_content_policy/fwdxoty/?utm_source=reddit&utm_medium=web2x&context=3&depth=2), unmoderated spaces on Reddit are an area we want to improve, from Modmail to PM’s, and political ads pose a unique challenge.\n\nIf the OP of a political ad (i.e., a campaign) moderates the comments, it’s problematic: they might remove dissenting perspectives. And if we (the admins) moderate the comments of a political ad, it’s even more problematic, putting us in the position of either moderating too much or too little, with inevitable accusations of bias either way.\n\nThe problem, we realized, is similar to what we see in r/announcements: lots of people commenting on a highly visible post outside the context of a community. It’s fair to say that r/announcements isn’t really a community; it lacks the culture, cohesion, and moderation that benefit most other subreddits, and as a result, the quality of conversation has deteriorated as the audience has grown.\n\nUltimately, conversations really only happen in the context of a community, and neither r/announcements nor political ads with comments on provide this. We believe we can foster better discussion on both with a different approach.\n\n## What we’re testing today\n\nInstead of having the usual free-for-all of comments on the r/announcements post itself, we are trying out a new experience today that encourages discussion of this post within other communities—an approach we hope works for political ads as well.\n\nBelow is a stickied comment with a link to submit this post to other communities on Reddit and a list of those discussion posts. The stickied comment will update automatically with new posts.\n\nA few other details to note for this test:\n\n* **The discussion posts are like any other post**, which means they can be voted on by users and removed by mods.\n* **Communities that don’t want to participate don’t have to.** (If you’re a mod of a community where a user attempts to crosspost this, you will get a Modmail alerting you to this with [opt-out instructions](https://www.reddit.com/r/modnews/comments/ilc4zc/testing_a_new_admin_post_type/).)\n* **Individual community rules apply to these posts just as any other**, so read the rules before attempting to bring the discussion into a completely unrelated community.\n* **Our stickied comment will link to discussions only from communities subject to our ads allow list.** Communities that have already opted not to appear in r/all won’t appear in the comment either, even if there is a discussion of this post there.\n* **After today’s test, we will likely test this system with political ads.**\n\nThis test will be a success if there are a variety of posts and conversations about this post, even—and perhaps particularly—if they are critical.\n\n## How we’re answering questions\n\nr/announcements posts have an important difference from political ads: I treat them as AMAs and do my best to answer questions and respond to criticism (both of which I appreciate). With this approach, I expect doing so will be more difficult (at least this first time). However, the point of this test is not to make you hunt for our answers or for us to reply to fewer questions, and we don’t intend to use this approach for all our admin posts (e.g., in r/ModNews, r/changelog, r/ModSupport, and others, which are smaller subreddits that still work well).\n\nFor today, we’re going to make the first link of this post to r/ModNews and start by answering mods’ questions there. In a future announcement, we may ask a specific community if they would host us for the discussion that day (depending on what the announcement is) and set that as an official destination for discussion, like a regular AMA.\n\nAdditionally, I’ll do my best to find other places to respond, and we’ll maintain another comment below this post to list replies we’ve given outside of r/announcements so you can easily find our responses (which was a feature request from [our post](https://www.reddit.com/r/modnews/comments/ilc4zc/testing_a_new_admin_post_type/g3r4xpm/) last week).\n\nUltimately, the goal of this test is to enable Reddit to do what Reddit does best: facilitate conversations (within the context of a community), provide commentary on political ads the way redditors already do on news and politics daily (sharing more information and calling bullshit in the comments when necessary), and extend the discussion well beyond the scope of the original post.\n\nThank you for participating. We hope this approach sets the stage for successful commentary not just today but down the road on political ads as well.\n\nSteve\n\n&#x200B;\n\n**Edit (9/28/20):** Update: After initial testing and a few small tweaks to the sorting and score display of the links in stickied comments like the one below, we’ll be using this discussion system on political ads moving forward. \n\nAs I mentioned, our goal with this approach was to encourage these types of discussions to happen within the context of a community. While this feature is completely optional for communities (opt-out instructions [here](https://www.reddit.com/r/modnews/comments/ilc4zc/testing_a_new_admin_post_type/)), we were pleased overall with the level of engagement that we saw from communities and users on this test post.\n\nWe’re still exploring how we’ll use this feature for r/announcements posts and how we can work with specific communities to have discussions about them. In the meantime, you can see our updated political ads policy on our [Advertising Policy Help Page](https://advertising.reddithelp.com/en/categories/reddit-advertising-policy/reddit-advertising-policy-overview).",
            "subreddit": {"_id": "2r0ij", "display_name": "announcements"},
            "title": "Today we’re testing a new way to discuss political ads (and announcements)",
            "upvote_ratio": 0.56,
            "url": "https://www.reddit.com/r/announcements/comments/ipitt0/today_were_testing_a_new_way_to_discuss_political/",
        },
        {
            "author": {"_id": "w7v6i", "name": "TinyTheT"},
            "comments": [
                {
                    "_id": "gbmcfn6",
                    "body": "If you are visiting /r/tattoos for the first time, or visiting from /r/all, Warning please be aware of ALL of the rules in the sidebar and stickied threads before posting. Common issues that ***WILL get you banned*** are any comments on **personal appearance**, any discussion about **pricing** of any kind, **aftercare/medical advice** or questions, and **trolling**.\n\n\n*I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/tattoos) if you have any questions or concerns.*",
                    "created_utc": 1604850427,
                    "author": {"_id": "6l4z3", "name": "AutoModerator"},
                    "score": 1,
                }
            ],
            "created_utc": 1604850426,
            "name": "t3_jqdso9",
            "score": 3,
            "selftext": "&#x200B;\n\nhttps://preview.redd.it/bx4eilepe1y51.png?width=1138&format=png&auto=webp&s=6bcd35127200225651a1b6946d0c7c82d56a2336",
            "subreddit": {"_id": "2qj9g", "display_name": "tattoos"},
            "title": "Yoshi Sticker Tattoo done by Timmy at Brand Ink in Germany, Bavaria",
            "upvote_ratio": 1,
            "url": "https://www.reddit.com/r/tattoos/comments/jqdso9/yoshi_sticker_tattoo_done_by_timmy_at_brand_ink/",
        },
        {
            "author": {"_id": "6jb6r8c", "name": "kafyr"},
            "comments": [
                {
                    "_id": "gbm5i2c",
                    "body": "\nHey u/kafyr! If you receive any message request from a racist username with jews in it ,do not accept it and report us the username. Send us a modmail if you find any NSFW messages. [We are looking for new friends in our reddit chatroom! Click here to join!](https://s.reddit.com/channel/13257801_9aa6504f4de019a180dd10cc184c2a1907de27a3)\n\n\n*I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/MakeNewFriendsHere) if you have any questions or concerns.*",
                    "created_utc": 1604846211,
                    "author": {"_id": "6l4z3", "name": "AutoModerator"},
                    "score": 1,
                },
                {
                    "_id": "gbnlgqv",
                    "body": "have you been able to travel this year with covid restrictions?",
                    "created_utc": 1604871438,
                    "author": {"_id": "8gbg4a7x", "name": "Serious_Amoeba137"},
                    "score": 1,
                },
            ],
            "created_utc": 1604846211,
            "name": "t3_jqcpo0",
            "score": 5,
            "selftext": "I'm looking for friends, people who share my interests or are at least interesting to talk with.\n\nI'm a tech guy, I love coding, playing mmorpg and travel. I love different culture, i love asia and in particular Japan (I try to visit places in asia once/twice at year).\n\nI'm bi-curious, currently in an open relationship (inclined and curious in sharing), but this isn't a requisite for friendship.\n\nI'm open to anything, same or different time zone is ok. Language has to be English or Italian (I would like to learn japanese, but this is a different story).",
            "subreddit": {"_id": "2vfcm", "display_name": "MakeNewFriendsHere"},
            "title": "31M from Italy",
            "upvote_ratio": 1,
            "url": "https://www.reddit.com/r/MakeNewFriendsHere/comments/jqcpo0/31m_from_italy/",
        },
    ]
    db.submission.insert_many(submissions)
    rc = RedditClient(db)
    yield rc


def test_get_subreddit_list(rc):
    assert set(rc.get_subreddit_list()) == set(
        ["announcements", "tattoos", "MakeNewFriendsHere"]
    )


def test_get_username_list(rc):
    assert set(rc.get_username_list()) == set(
        ["spez", "AutoModerator", "TinyTheT", "kafyr", "Serious_Amoeba137"]
    )


def test_get_sorted_subreddit_count_list(rc):
    assert rc.get_sorted_subreddit_count_list() == [
        {"count": 1, "_id": "MakeNewFriendsHere"},
        {"count": 1, "_id": "announcements"},
        {"count": 1, "_id": "tattoos"},
    ]


def test_get_sorted_user_submission_count_list(rc):
    assert rc.get_sorted_user_submission_count_list() == [
        {"count": 1, "_id": "TinyTheT"},
        {"count": 1, "_id": "kafyr"},
        {"count": 1, "_id": "spez"},
    ]


def test_get_sorted_user_comment_count_list(rc):
    assert rc.get_sorted_user_comment_count_list() == [
        {"count": 3, "_id": "AutoModerator"},
        {"count": 1, "_id": "Serious_Amoeba137"},
        {"count": 1, "_id": "spez"},
    ]


def test_get_comment_id_list_by_username(rc):
    username = "AutoModerator"
    assert rc.get_comment_id_list_by_username(username) == [
        {"_id": "g4k3btr"},
        {"_id": "gbmcfn6"},
        {"_id": "gbm5i2c"},
    ]


def test_get_user_subreddit_from_submission_list(rc):
    assert rc.get_user_subreddit_from_submission_list() == [
        {"subreddit": ["tattoos"], "_id": "TinyTheT", "len": 1},
        {"subreddit": ["MakeNewFriendsHere"], "_id": "kafyr", "len": 1},
        {"subreddit": ["announcements"], "_id": "spez", "len": 1},
    ]


def test_get_user_subreddit_from_comment_list(rc):
    assert rc.get_user_subreddit_from_comment_list() == [
        {
            "subreddit": ["announcements", "tattoos", "MakeNewFriendsHere"],
            "_id": "AutoModerator",
            "len": 3,
        },
        {"subreddit": ["MakeNewFriendsHere"], "_id": "Serious_Amoeba137", "len": 1},
        {"subreddit": ["announcements"], "_id": "spez", "len": 1},
    ]


def test_get_user_subreddit_list_by_username(rc):
    username = "AutoModerator"
    assert set(rc.get_user_subreddit_list_by_username(username)) == set(
        [
            "tattoos",
            "announcements",
            "MakeNewFriendsHere",
        ]
    )
