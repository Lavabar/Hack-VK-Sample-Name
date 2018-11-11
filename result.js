require(Modules.ASR);

const say_config = Language.RU_RUSSIAN_FEMALE;
const myNumber = '78124256201';
var phone;
var myCall;
var question_id = 0;
var tasks = [
    // {
    //     music: 'https://psv4.vkuseraudio.net/c536213/u183259156/audios/c6789270db88.mp3?extra=dOPoZwwgmUC0PmJrQANSs_dB1pzXgcITWeTom8SzLhKUHr2O6JF8zOfTa3V3ksgNtqK7REvR_kQpBwt9plonzoNjSKwCHrqZ8WQpmI_OjZ-cBEup_-AhftV2OQWitsla0ARo63vbM_PuCyVnmyDpKw',
    //     question: 'Кто композитор данного произведения?',
    //     answers: [
    //         'рахманинов',
    //         'бах',
    //         'вивальди'
    //     ],
    //     roots: ['ахман'],
    //     right: 0
    // },
    {
        question: 'На каком инструменте играл итальянский композитор Вивальди?',
        answers: [
            'гитара',
            'скрипка',
            'фортепиано'
        ],
        roots: ['скрипк'],
        right: 1
    },
    {
        question: 'В каком городе был открыт первый памятник Михаилу Глинке?',
        answers: [
            'москва',
            'воронеж',
            'смоленск'
        ],
        roots: ['молен'],
        right: 2
    },
    {
        question: 'Где скончался композитор Рихард Вагнер?',
        answers: [
            'германия',
            'россия',
            'венеция'
        ],
        roots: ['енец'],
        right: 2
    }
]
var timer;
var is_right;

VoxEngine.addEventListener(AppEvents.Started, (e) => {
    phone = VoxEngine.customData();
    myCall = VoxEngine.callPSTN(phone, myNumber);
    myCall.addEventListener(CallEvents.Connected, startGame)
})

function startGame() {
    myCall.removeEventListener(CallEvents.Connected)
    myCall.say('Добро пожаловать на музыкальную викторину. У нас будет 5 вопросов. у вас будет по 5 секунд на ответ для каждого вопроса. И всего одна попытка.  Давайте начнем!', say_config);
    myCall.addEventListener(CallEvents.PlaybackFinished, askQuestion);
}

function askQuestion() {
    if (question_id != tasks.length)  {
        myCall.removeEventListener(CallEvents.PlaybackFinished);
        let answers_text = '';
        for (i = 0; i < tasks[question_id].answers.length; i++) {
            answers_text += tasks[question_id].answers[i] + '...  ';
        }
        if (!!tasks[question_id].music) {
            myCall.say('Вопрос номер: ' + (question_id + 1) + '...'  + tasks[question_id].question, say_config);
            myCall.addEventListener(CallEvents.PlaybackFinished, e => {
                myCall.removeEventListener(CallEvents.PlaybackFinished);
                myCall.startPlayback(tasks[question_id].music)
                setTimeout((e) => {
                    myCall.stopPlayback();
                    myCall.say('. Варианты ответов: ' + answers_text, say_config);
                    myCall.addEventListener(CallEvents.PlaybackFinished, (e) => {
                        myCall.removeEventListener(CallEvents.PlaybackFinished);
                        let myASR = VoxEngine.createASR({
                            lang: ASRLanguage.RUSSIAN_RU
                        });
                        myCall.sendMediaTo(myASR);
                        setTimeout((e) => {
                            myASR.removeEventListener(ASREvents.Result);
                            endQuestion(is_right);
                        }, 7000)
                        myASR.addEventListener(ASREvents.Result, (e) => {
                            myASR.removeEventListener(ASREvents.Result);
                            myASR.stop(); 
                            is_right = isRight(e.text);
                        })
                    })                
                }, 7000)
            })
        }
        else {
            myCall.say('Вопрос номер: ' + (question_id + 1) + '...  ' + tasks[question_id].question + '. Варианты ответов: ' + answers_text, say_config);
            myCall.addEventListener(CallEvents.PlaybackFinished, (e) => {
                myCall.removeEventListener(CallEvents.PlaybackFinished);
                let myASR = VoxEngine.createASR({
                    lang: ASRLanguage.RUSSIAN_RU
                });
                myCall.sendMediaTo(myASR);
                setTimeout((e) => {
                    myASR.removeEventListener(ASREvents.Result);
                    endQuestion(is_right);
                }, 7000)
                myASR.addEventListener(ASREvents.Result, (e) => {
                    myASR.removeEventListener(ASREvents.Result);
                    myASR.stop(); 
                    is_right = isRight(e.text);
                })            
            })
        }
    }
    else winGame();
    
}

//Конец вопроса
function endQuestion(bool) {
    let text_right = bool ? 'Поздравляю вы правильно ответили на этот вопрос. Продолжайте в том же духе!' : 'К сожалению вы дали неправильный ответ. Возможно вам повезет в следующий раз. Всего доброго';
    myCall.say(`Время вышло. Внимание, правильный ответ: ${tasks[question_id].answers[tasks[question_id].right]}. ${text_right}.`, say_config) 
    myCall.addEventListener(CallEvents.PlaybackFinished, (e) => {
        myCall.removeEventListener(CallEvents.PlaybackFinished);
        question_id++;
        if (bool) askQuestion()
        else VoxEngine.terminate()
    })
}
function isRight(text) {
    return tasks[question_id].roots.every(root => {
        return text.toLowerCase().includes(root)
    })
}

function winGame() {
    myCall.say('Поздравляю! Вы победили! Всего хорошего!', say_config);
    myCall.addEventListener(CallEvents.PlaybackFinished, VoxEngine.terminate)
}
