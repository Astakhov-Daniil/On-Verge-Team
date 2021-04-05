let AllPlayersData = new Array(100)

document.getElementById('but_file').addEventListener('click', function() {

    let reader = new FileReader()

    reader.readAsText(document.getElementById('file').files[0])

    AllPlayersData = reader.onload = function() {
        let MainStrMas = String(reader.result).split('END')

        let PlayerStrMas = ' '

        for (let i = 1; i < 4; i++) {

            PlayerStrMas = MainStrMas[i - 1].split('PARTY')

            let dir = document.getElementById('player' + String(i))

            let img = document.createElement('img')
            img.src = 'img/Top_players' + String(i) + '.png'

            let h3 = document.createElement('h3')
            h3.innerHTML = PlayerStrMas[0].trim()

            let button = document.createElement('button')
            button.setAttribute('class', 'butPlayer')
            button.innerHTML = 'Партии ' + PlayerStrMas[0]

            dir.appendChild(img)
            dir.appendChild(h3)
            dir.appendChild(button)

            AllPlayersData[i - 1] = new Array(3)
            AllPlayersData[i - 1][0] = PlayerStrMas[0]
            AllPlayersData[i - 1][1] = PlayerStrMas[1]
            AllPlayersData[i - 1][2] = PlayerStrMas[2]
        }

        let ol = document.getElementById('players')

        let img_index = 1
        for (let i = 4; i < 101; i++) {

            PlayerStrMas = MainStrMas[i - 1].split('PARTY')

            let li = document.createElement('li')
            li.classList.add('otherplayers')

            let h2 = document.createElement('h2')
            h2.innerHTML = i

            let h3 = document.createElement('h3')
            h3.innerHTML = PlayerStrMas[0].trim()

            let img = document.createElement('img')
            img.src = 'img/iconPlayer' + String(img_index) + '.jpg'

            let button = document.createElement('button')
            button.setAttribute('class', 'butPlayer')
            button.innerHTML = 'Партии ' + PlayerStrMas[0]

            ol.appendChild(li)
            li.appendChild(h2)
            li.appendChild(img)
            li.appendChild(h3)
            li.appendChild(button)
            if (img_index == 15) {
                img_index = 1
            } else {
                img_index++
            }
            AllPlayersData[i - 1] = new Array(3)
            AllPlayersData[i - 1][0] = PlayerStrMas[0]
            AllPlayersData[i - 1][1] = PlayerStrMas[1]
            AllPlayersData[i - 1][2] = PlayerStrMas[2]

            let PS = document.getElementById('downoadFile')
            PS.textContent = 'Загружена!'
        }
        let ButArray = document.getElementsByClassName('butPlayer')

        for (let i = 0; i < ButArray.length; i++) {

            ButArray[i].onclick = function() {

                let player = this.innerHTML.slice(this.innerHTML.indexOf(' ') + 1)
                player = player.trim()

                for (let j = 0; j < 100; j++) {

                    if (AllPlayersData[j][0].indexOf(player) !== -1) {

                        let Pole = document.getElementById('pole')
                        Pole.classList.remove('gamepoleEmpty')
                        Pole.classList.add('gamepole')

                        let h3 = document.createElement('h3')
                        h3.innerHTML = 'Выерите партию игрока'

                        let button1 = document.createElement('button')
                        button1.setAttribute('id', 1)
                        button1.innerHTML = 'Последняя партия'

                        let button2 = document.createElement('button')
                        button2.setAttribute('id', 2)
                        button2.innerHTML = 'Предпоследняя партия'


                        let buttonEnd = document.createElement('button')
                        buttonEnd.setAttribute('id', 3)
                        buttonEnd.innerHTML = 'Закрыть окно'

                        let img = document.createElement('img')
                        img.src = 'img/StartParty.png'

                        Pole.appendChild(h3)
                        Pole.appendChild(button1)
                        Pole.appendChild(button2)
                        Pole.appendChild(buttonEnd)
                        Pole.appendChild(img)

                        buttonEnd.onclick = function() {
                            button1.remove()
                            button2.remove()
                            buttonEnd.remove()
                            img.remove()
                            Pole.classList.remove('gamepole')
                            Pole.classList.add('gamepoleEmpty')
                        }

                        button1.onclick = function() {

                            let game = AllPlayersData[j][1].split('\n')

                            img.src = 'img/pole.png'
                            h3.textContent = String(game[1] + game[2])

                            let h4_1 = document.createElement('h4')
                            h4_1.innerHTML = 'Тип партии: ' + game[3].slice(0, game[3].indexOf(' '))

                            let h4_2 = document.createElement('h4')
                            h4_2.innerHTML = 'Результат: ' + game[3].slice(game[3].indexOf(' '), game[3].length)

                            let h4_3 = document.createElement('h4')
                            h4_3.innerHTML = game[5]

                            button1.remove()
                            button2.remove()
                            buttonEnd.innerHTML = 'Закрыть окно'

                            Pole.appendChild(h4_1)
                            Pole.appendChild(h4_2)
                            Pole.appendChild(h4_3)

                            let line = document.createElement('div')
                            line.setAttribute('class', 'linetochka')

                            if (game[4].indexOf('B') == -1 && game[4].indexOf('W') == -1) {
                                h3.textContent = 'Нет данных о ходах'
                            } else {
                                Mas_Data = game[4].split('.')

                                for (let line_index = 0; line_index < 400; line_index++) {

                                    let toch = document.createElement('div')
                                    toch.setAttribute('class', 'tochka')

                                    for (let i_Pole = 0; i_Pole < 19 * 19; i_Pole++) {

                                        y_Pole = img_index / 19
                                        x_Pole = i_Pole - (19 * y_Pole) - 1
                                        Mas_motion = Mas_Data[i_Pole].split("")

                                        for (let mx = 0; mx < Mas_Data.length; mx++) {

                                            if (Mas_motion[1].codePointAt(0) - 97 == x_Pole) {
                                                if (Mas_motion[2].codePointAt(0) - 97 == y_Pole) {
                                                    if (Mas_motion[0] == 'B') {
                                                        toch.style.backgroundColor = ('black')
                                                    }
                                                    if (Mas_motion[0] == 'W') {
                                                        toch.style.backgroundColor = ('white')
                                                    }

                                                }
                                            }
                                        }

                                        line.appendChild(toch)
                                    }
                                }
                            }

                            buttonEnd.onclick = function() {

                                line.remove()
                                h3.remove()
                                img.remove()
                                h4_1.remove()
                                h4_2.remove()
                                h4_3.remove()
                                buttonEnd.remove()

                                Pole.classList.remove('gamepole')
                                Pole.classList.add('gamepoleEmpty')
                            }
                        }

                        button2.onclick = function() {

                            let game = AllPlayersData[j][2].split('\n')

                            img.src = 'img/pole.png'
                            h3.textContent = String(game[1] + game[2])

                            let h4_1 = document.createElement('h4')
                            h4_1.innerHTML = 'Тип партии: ' + game[3].slice(0, game[3].indexOf(' '))

                            let h4_2 = document.createElement('h4')
                            h4_2.innerHTML = 'Результат: ' + game[3].slice(game[3].indexOf(' '), game[3].length)

                            let h4_3 = document.createElement('h4')
                            h4_3.innerHTML = game[5]

                            button1.remove()
                            button2.remove()
                            buttonEnd.innerHTML = 'Закрыть окно'

                            Pole.appendChild(h4_1)
                            Pole.appendChild(h4_2)
                            Pole.appendChild(h4_3)

                            let line = document.createElement('div')
                            line.setAttribute('class', 'linetochka')

                            Main_motion = game[4].split('.')
                            let Toch_Mas = new Array(400)
                            for (let line_index = 0; line_index < 400; line_index++) {

                                let toch = document.createElement('div')
                                toch.setAttribute('class', 'tochka')
                                Toch_Mas[line_index] = toch
                                line.appendChild(toch)
                            }

                            Pole.appendChild(line)

                            for (let g = 0; g < Main_motion.length; g++) {

                                motion = Main_motion[g].split('')
                                console.log(motion)

                                let X = String(motion[1]).charCodeAt(0) - 97
                                let Y = String(motion[2]).charCodeAt(0) - 97
                                if (motion[0] == 'B') {
                                    Toch_Mas[X][20 * X + Y].style.backgroundColor = ('black')
                                    console.log('black')
                                }
                                if (motion[0] == 'W') {
                                    Toch_Mas[X][20 * X + Y].style.backgroundColor = ('white')
                                    console.log('black')
                                }
                            }

                            buttonEnd.onclick = function() {

                                line.remove()
                                h3.remove()
                                img.remove()
                                h4_1.remove()
                                h4_2.remove()
                                h4_3.remove()
                                buttonEnd.remove()

                                Pole.classList.remove('gamepole')
                                Pole.classList.add('gamepoleEmpty')
                            }
                        }
                    }
                }
            }
        }
    }
})