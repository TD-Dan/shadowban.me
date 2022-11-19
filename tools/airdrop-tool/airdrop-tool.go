package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	twitter "github.com/g8rswimmer/go-twitter/v2"
)

type authorize struct {
	Token string
}

func (a authorize) Add(req *http.Request) {
	req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", a.Token))
}

/*
*

	In order to run, the user will need to provide the bearer token and the list of tweet ids.

*
*/
func main() {
	help := flag.Bool("help", false, "show help")
	tool := flag.String("tool", "", "tool to use")
	ids := flag.String("ids", "", "tweet id(s)")
	token := flag.String("token", "", "twitter API token")
	flag.Parse()

	if *help || *tool == "" {
		fmt.Printf("\nUsage: -tool <tool> -<tool parameters>")
		fmt.Printf("\n    getweets -ids tweet_id(s) -token TWITTER_API_TOKEN\n")
		fmt.Printf("\n    getcomments -ids tweet_id -token TWITTER_API_TOKEN\n")
		return
	}

	switch *tool {
	case "gettweets":
		gettweets(*ids, *token)
	case "getcomments":
		getcomments(*ids, *token)
	default:
		fmt.Printf("%s is not a tool", *tool)
	}

}

func gettweets(ids string, token string) {
	fmt.Printf("Fetching tweets %s...\n", ids)

	if token == "" || ids == "" {
		log.Panicf("id and token arguments missing")
	}

	client := &twitter.Client{
		Authorizer: authorize{
			Token: token,
		},
		Client: http.DefaultClient,
		Host:   "https://api.twitter.com",
	}
	opts := twitter.TweetLookupOpts{
		Expansions:  []twitter.Expansion{twitter.ExpansionEntitiesMentionsUserName, twitter.ExpansionAuthorID},
		TweetFields: []twitter.TweetField{twitter.TweetFieldCreatedAt, twitter.TweetFieldConversationID, twitter.TweetFieldAttachments},
	}

	fmt.Println("Callout to tweet lookup callout")

	tweetResponse, err := client.TweetLookup(context.Background(), strings.Split(ids, ","), opts)
	if err != nil {
		log.Panicf("tweet lookup error: %v", err)
	}

	dictionaries := tweetResponse.Raw.TweetDictionaries()

	enc, err := json.MarshalIndent(dictionaries, "", "    ")
	if err != nil {
		log.Panic(err)
	}
	fmt.Println(string(enc))
}

func getcomments(ids string, token string) {
	fmt.Printf("Fetching comments for %s...\n", ids)

	if token == "" || ids == "" {
		log.Panicf("ids and token arguments missing")
	}

	client := &twitter.Client{
		Authorizer: authorize{
			Token: token,
		},
		Client: http.DefaultClient,
		Host:   "https://api.twitter.com",
	}
	opts := twitter.TweetRecentSearchOpts{
		Expansions:  []twitter.Expansion{twitter.ExpansionEntitiesMentionsUserName, twitter.ExpansionAuthorID},
		TweetFields: []twitter.TweetField{twitter.TweetFieldCreatedAt, twitter.TweetFieldConversationID, twitter.TweetFieldAttachments},
		//MaxResults:  10,
		//NextToken: ,
	}

	query := "conversation_id:" + ids

	fmt.Printf("Callout to tweet recent search with: %s\n", query)

	batch_size := 100
	max_batches := 5
	batch_wait_seconds := 1.5
	all_tweets := map[string]*twitter.TweetDictionary{}
	for n := 1; n <= max_batches; n++ {

		opts.MaxResults = batch_size

		tweetResponse, err := client.TweetRecentSearch(context.Background(), query, opts)
		if err != nil {
			log.Panicf("tweet lookup error: %v", err)
		}

		dictionaries := tweetResponse.Raw.TweetDictionaries()

		for k, v := range dictionaries {
			all_tweets[k] = v
		}

		/*enc, err := json.MarshalIndent(dictionaries, "", "    ")
		if err != nil {
			log.Panic(err)
		}
		fmt.Println(string(enc))*/

		metaBytes, err := json.MarshalIndent(tweetResponse.Meta, "", "    ")
		if err != nil {
			log.Panic(err)
		}
		fmt.Println(string(metaBytes))

		fmt.Println(tweetResponse.RateLimit)

		opts.NextToken = tweetResponse.Meta.NextToken
		if opts.NextToken == "" {
			break
		}

		time.Sleep(time.Duration(batch_wait_seconds) * time.Second)

	}

	fmt.Printf("Done: Fetched %v comments", len(all_tweets))

	jsonString, err := json.MarshalIndent(all_tweets, "", "    ")
	if err != nil {
		log.Panic(err)
	}

	ioutil.WriteFile("comments.json", jsonString, os.ModePerm)

}
