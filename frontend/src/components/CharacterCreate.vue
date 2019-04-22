<template>
<div id="character-create">
    <form @submit="handleSave">
        <div class="columns">
            <div class="column">
                <div class="field">
                    <div class="control">
                        <button class="button is-outlined is-link">
                            <span>
                                Create
                            <font-awesome-icon icon="plus-square"></font-awesome-icon>
                            </span>
                        </button>
                    </div>
                </div>
                <div class="field">
                    <label for="is_player" class="checkbox">
                        Player
                        <input type="checkbox" v-model="character.is_player" :class=" {'is-danger': errors.is_player}">
                    </label>
                    <p
                        class="help is-danger"
                        v-for="error in errors.is_player"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>
                <div class="field">
                    <label class="field-label is-normal" for="name">Name</label>
                    <div class="field-body">
                        <input class="input" id="name" type="text" v-model="character.name" required :class=" {'is-danger': errors.name}">
                    </div>
                    <p
                        class="help is-danger"
                        v-for="error in errors.name"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>
                <div class="field">
                    <label class="field-label is-normal" for="hit_dice">Hit dice</label>
                    <div class="field-body">
                        <input class="input" id="hit_dice" type="text" v-model="character.hit_dice" :disabled="character.is_player" :class=" {'is-danger': errors.hit_dice}">
                    </div>
                    <p
                        class="help is-danger"
                        v-for="error in errors.hit_dice"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>
            </div>
            <div class="column">
                <h2 class="subtitle">Load template</h2>
                <PathfinderMonsterImport
                    @pathfinder-monster-chosen="onPathfinderMonsterChosen"
                ></PathfinderMonsterImport>
            </div>
        </div>
        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="field-label is-normal" for="description">Description</label>
                    <div class="field-body">
                        <textarea class="textarea" id="description" v-model="character.description" v-autosize="character.description" :class=" {'is-danger': errors.description}"></textarea>
                    </div>
                    <p
                        class="help is-danger"
                        v-for="error in errors.description"
                        :key="error"
                    >
                        {{ error }}
                    </p>
                </div>

            </div>
            <div class="column">
                <vue-markdown class="content" :source="character.description"></vue-markdown>
            </div>
        </div>
    </form>
</div>
</template>

<script>
const PathfinderMonsterImport = () => import('./PathfinderMonsterImport.vue');
const VueMarkdown = () => import('vue-markdown');

export default {
    name: 'CharacterCreate',
    components: { PathfinderMonsterImport, VueMarkdown },
    data() {
        return {
            character: {
                is_player: false,
                name: '',
                hit_dice: '',
                description: '',
            },
            errors: {},
        }
    },
    methods : {
        handleSave(e) {
            e.preventDefault();
            let vm = this;
            let postData = {
                name: this.character.name,
                is_player: this.character.is_player,
                description: this.character.description
            };
            if (!this.character.is_player) {
                postData.hit_dice = this.character.hit_dice;
            }
            this.$http.post(
                '/api/characters/',
                postData
            ).then((response) => {
                vm.errors = {}
                vm.character = response.data;
                vm.$router.push({name: 'character', params: {uuid: vm.character.uuid}});
            }).catch((error) => {
                vm.errors = error.response.data;
            });
        },
        onPathfinderMonsterChosen(event) {
            let subtypes = '' 
            if (event.subtypes.length > 0) {
                subtypes = `(${event.subtypes.join(', ')})`;
            }
            let feats = '';
            if (event.feats.length > 0) {
                feats = `${event.feats.join(', ')}`;
            }
            let skills = '';
            console.log(event.skills);
            if (Object.keys(event.skills).length > 0) {
                let tmp_skills = [];
                for (var skill of Object.keys(event.skills)) {
                    tmp_skills.push(`${skill} ${event.skills[skill]}`);
                }
                skills = `${tmp_skills.join(', ')}`;
            }
            this.character.is_player = false;
            this.character.name = event.name;
            this.character.hit_dice = event.hit_dice;
            this.character.description = 
`**CR** ${event.cr} | **XP** ${event.xp}
${event.alignment} ${event.size} ${event.type} ${subtypes}
**Init** ${event.initiative}; **Senses** ???
**Pereception** ${event.perception}

Defense
-------
**AC** ${event.ac}, **touch** ${event.ac_touch}, **float-footed** ${event.ac_flat_footed}
**hp** ${event.hp} (${event.hit_dice})
**Fort** ${event.fortitude_save}, **Ref** ${event.reflex_save}, **Will** ${event.will_save}
**DR** ???

Offense
-------
**Speed** ${event.speed}
**Melee** ${event.melee_attack}
**Reach** ${event.reach} ft.
**Ranged** ${event.ranged_attack}

Statistics
----------
**Str** ${event.strength}, **Dex** ${event.dexterity}, **Con** ${event.constitution}, **Int** ${event.intelligence}, **Wis** ${event.wisdom}, **Cha** ${event.charisma}
**Base Atk** ???, **CMB** ???, **CMD** ???
**Feats** ${feats}
**Skills** ${skills}
**Modifiers** ${event.racial_mods}
**Languages** ${event.languages}
**SQ** ${event.special_qualities}

Ecology
-------
**Environment** ${event.environment}
**Organization** ${event.organization}
**Treasure** ${event.treasure}
`;
        }
    }
}
</script>

<style scoped>
</style>
