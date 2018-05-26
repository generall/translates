var vueDiff = new Vue({
    el: '#diff',
    data: {
        orig: "Hello, I am Andrew",
        translation: 'Привет, я Андрей',
        yandex_translation: '',
        userText: "",
        diff: [],
        count: 0
    },
    methods: {
        calcDiff: function (oldStr, newStr) {
            var diff = JsDiff.diffWords(oldStr, newStr, { ignoreCase: true })
            diff.forEach(element => element.hint = "...");
            this.diff = diff;
        },
        updDiff: function() {
            this.calcDiff(this.orig, this.userText)
        },
        loadNext: function(){
            this.$http.get('/get_next').then(response => {
                this.orig = response.body.en_text;
                this.translation = response.body.ru_text_orig;
                this.yandex_translation = response.body.ru_text_translate;
                this.userText = '';
                this.diff = [];
            })

        },
        commit: function(){
            this.$http.post('/commit', {
                en_text: this.orig,
                user_text: JSON.stringify(this.diff)
            }).then(response => {
                this.orig = response.body.en_text;
                this.translation = response.body.ru_text_orig;
                this.yandex_translation = response.body.ru_text_translate;
                this.userText = '';
                this.diff = [];
                this.count += 1;
            })
        },
        showHint: function(item) {
            console.log(item);
            item.hint = item.value;
        }
    }
})

vueDiff.loadNext()

// let oldStr = "Hello, I am Andrew"
// let newStr = "Hello, I an andrew"

// vueDiff.calcDiff(oldStr, newStr)