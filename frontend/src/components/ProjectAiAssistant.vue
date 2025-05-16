<template>
  <div class="musicdibs-card mx-auto w-full rounded-box bg-base-100 shadow-lg">
    <div class="card-body space-y-4">
      <h2 class="card-title">Asistente IA</h2>

      <p v-if="status == 'in_progress'" class="text-base-content/70 text-sm">
        Utiliza este asistente para ayudarte en la creación de tu proxima obra
        maestra.
      </p>
      <p v-else>
        Estes son los datos en que se ha basado el asistente para generar tu
        obra:
      </p>

      <div class="space-y-1text-sm">
        <p>
          <span class="font-semibold">Propósito:</span>
          {{ project.conversation?.purpose || "-" }}
        </p>
        <p>
          <span class="font-semibold">Tempo:</span>
          {{ project.conversation?.tempo || "-" }} BPM
        </p>
        <p>
          <span class="font-semibold">Armadura de tonalidad:</span>
          {{ project.conversation?.key_signature || "-" }}
        </p>
        <p>
          <span class="font-semibold">Estado de ánimo:</span>
          {{ project.conversation?.mood || "-" }}
        </p>
      </div>

      <div
        class="chat-container max-h-[70vh] space-y-2 overflow-y-auto rounded-md border border-gray-300 p-3"
        ref="chatContainer"
      >
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['chat', msg.is_from_ai ? 'chat-start' : 'chat-end']"
        >
          <div
            class="chat-bubble-custom chat-bubble"
            v-if="msg.is_from_ai"
            v-html="formatText(msg.content)"
          ></div>
          <div class="chat-bubble-custom chat-bubble" v-else>
            {{ msg.content }}
          </div>
        </div>
        <div v-if="isLoading && sentMessage != ''" class="chat chat-end">
          <div class="chat-bubble-custom chat-bubble">{{ sentMessage }}</div>
        </div>
        <span v-if="isLoading" class="loading loading-ring loading-lg"></span>
      </div>

      <template v-if="status == 'in_progress'">
        <form
          @submit.prevent="handleSendMessage"
          class="flex flex-col items-end gap-2 sm:flex-row"
        >
          <textarea
            v-model="newMessage"
            class="textarea-bordered textarea w-full"
            placeholder="Escribe tu mensaje aquí..."
            rows="2"
            :disabled="isLoading"
          ></textarea>

          <button
            type="submit"
            class="btn btn-primary"
            :disabled="isLoading || !newMessage.trim()"
          >
            {{ isLoading ? "Enviando..." : "Enviar" }}
          </button>
        </form>

        <div class="flex items-center">
          <button
            class="btn btn-primary btn-outline btn-wide mr-4"
            @click="handleFinishConversation"
            :disabled="isLoading"
          >
            Finalizar conversación
          </button>
          <p>
            Si estas contento con lo que el asistente ha generado, pincha el
            botón a continuación para finalizar la conversación y poder
            registrar la obra. Una vez finalizado, no se puede volver a acceder
            a esta conversación.
          </p>
        </div>
      </template>
      <p v-else>Este asistente ya ha sido completado, y no se puede cambiar.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from "vue";

const props = defineProps({
  project: Object,
  messages: {
    type: Array,
    default: () => [],
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  status: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["sendMessage", "finishConversation"]);

const newMessage = ref("");
const sentMessage = ref("");
const chatContainer = ref(null);

// Scroll to bottom function using Vue's ref system
const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

// Watch for changes in messages to scroll to bottom
watch(
  () => [props.messages, props.isLoading],
  () => {
    scrollToBottom();
  },
  { deep: true },
);

watch(
  () => props.messages,
  (messages) => {
    console.log("messages", messages);
    if (messages.length === 0 && !newMessage.value) {
      newMessage.value = props.project?.description || "";
    } else {
      newMessage.value = "";
    }
  },
  { immediate: true },
);

onMounted(() => {
  scrollToBottom();
});

const handleSendMessage = (e) => {
  if (newMessage.value.trim() && !props.isLoading) {
    emit("sendMessage", newMessage.value.trim());
    sentMessage.value = newMessage.value;
    newMessage.value = "";
  }
};

const handleFinishConversation = () => {
  if (!props.isLoading) {
    emit("finishConversation");
  }
};

const formatText = (text) => {
  const marker = "--- LA OBRA ---";
  if (!text.includes(marker)) return text;

  const parts = text.split(marker);

  return `<p>${parts[0].trim()}</p>
    <div class="text-center my-4">${marker}</div>
    <p>${parts[1]?.trim().replaceAll("\n", "<br />")}</p>
    <div class="text-center my-4">${marker}</div>`;
};
</script>
