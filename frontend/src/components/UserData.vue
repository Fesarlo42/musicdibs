<template>
  <div class="musicdibs-card bg-base-100">
    <div class="card-body">
      <h2 class="card-title">Tus datos</h2>
      <section v-if="error">
        <div v-if="error" role="alert" class="alert alert-soft alert-error">
          <span>{{ error }}</span>
        </div>
      </section>
      <p>Pincha en la información que deseas editar.</p>
      <template v-if="userData && userData.id">
        <div class="grid-cols-2 gap-8 md:grid">
          <div>
            <fieldset class="fieldset">
              <legend class="fieldset-legend">Nombre</legend>
              <div @click="startEditing('first_name')">
                <template v-if="editingField === 'first_name'">
                  <input
                    v-model="form.first_name"
                    class="input"
                    @input="handleInput"
                    @blur="stopEditing"
                    autofocus
                  />
                </template>
                <template v-else>
                  <p class="cursor-pointer">{{ form.first_name }}</p>
                </template>
              </div>
            </fieldset>

            <fieldset class="fieldset">
              <legend class="fieldset-legend">Apellidos</legend>
              <div @click="startEditing('last_name')">
                <template v-if="editingField === 'last_name'">
                  <input
                    v-model="form.last_name"
                    class="input"
                    @input="handleInput"
                    @blur="stopEditing"
                    autofocus
                  />
                </template>
                <template v-else>
                  <p class="cursor-pointer">{{ form.last_name }}</p>
                </template>
              </div>
            </fieldset>
          </div>

          <div>
            <fieldset class="fieldset">
              <legend class="fieldset-legend">Correo electrónico</legend>
              <div @click="startEditing('email')">
                <template v-if="editingField === 'email'">
                  <input
                    v-model="form.email"
                    class="input"
                    type="email"
                    @input="handleInput"
                    @blur="stopEditing"
                    autofocus
                  />
                </template>
                <template v-else>
                  <p class="cursor-pointer">{{ form.email }}</p>
                </template>
              </div>
            </fieldset>

            <fieldset class="fieldset">
              <legend class="fieldset-legend">Contraseña</legend>
              <div @click="startEditing('password')">
                <template v-if="editingField === 'password'">
                  <input
                    v-model="form.password"
                    class="input"
                    type="password"
                    @input="handleInput"
                    @blur="stopEditing"
                    autofocus
                  />
                </template>
                <template v-else>
                  <p class="cursor-pointer">Cambiar contraseña</p>
                </template>
              </div>
            </fieldset>
          </div>
        </div>

        <div v-if="isChanged" class="mt-6">
          <button class="btn btn-primary" @click="handleSave">
            Guardar cambios
          </button>
          <button class="btn btn-primary btn-soft" @click="handleReset">
            Cancelar
          </button>
        </div>
      </template>
      <template v-else>
        <p class="text-center">
          Hubo un problema al recuperar tus datos. Vuelve a intentar.
        </p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from "vue";

const props = defineProps({
  userData: {
    type: Object,
  },
  error: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(["saveForm"]);

const editingField = ref(null);
const isChanged = ref(false);

const form = reactive({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
});

watch(
  () => props.userData,
  (newVal) => {
    if (newVal && newVal.id) {
      form.first_name = newVal.first_name || "";
      form.last_name = newVal.last_name || "";
      form.email = newVal.email || "";
      form.password = "";
    }
  },
  { immediate: true }, // run immediately in case userData is already set
);

const startEditing = (field) => {
  editingField.value = field;
};

const stopEditing = () => {
  editingField.value = null;
};

const handleInput = () => {
  isChanged.value = true;
};

const handleSave = async () => {
  emit("saveForm", { ...form });

  isChanged.value = false;
  stopEditing();
};

const handleReset = () => {
  form.first_name = props.userData.first_name;
  form.last_name = props.userData.last_name;
  form.email = props.userData.email;
  form.password = "";

  isChanged.value = false;
  stopEditing();
};
</script>
